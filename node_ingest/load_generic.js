const fs = require('fs');
const csv = require('csv-parser');
const pool = require('./db');

const csvFile = process.argv[2];
const tableName = process.argv[3];

if (!csvFile || !tableName) {
    console.error("Использование: node load_generic.js <csv_файл> <имя_таблицы>");
    process.exit(1);
}

function fixNumber(v) {
    if (v === undefined || v === null) return null;
    if (v === '' || v.trim() === '' || v === '-' || v === 'NaN' || v === 'N/A')
        return null;

    // Если внутри есть запятая, мы ее убираем (например, 1,234 → 1234)
    const cleaned = v.replace(/,/g, '');
    if (!isNaN(cleaned)) return cleaned;
    return null;
}

function fixDate(v) {
    if (!v) return null;

    // CSV format: M/D/YY
    const parts = v.split('/');
    if (parts.length !== 3) return v;

    const [m, d, yy] = parts;
    const yyyy = Number(yy) < 50 ? `20${yy}` : `19${yy}`;

    return `${yyyy}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
}

async function loadData() {
    const rows = [];
    let hdrs = [];

    fs.createReadStream(`../data/${csvFile}`)
        .pipe(csv())
        .on('headers', headers => {
            hdrs = headers;
            console.log('Найденные столбцы:', hdrs);
        })
        .on('data', row => rows.push(row))
        .on('end', async () => {
            console.log(`${rows.length} Найдены строки. Вставить начальную...`);
            const quotedColumns = hdrs.map(c => `"${c}"`).join(', ');
            const placeholders = hdrs.map((_, i) => `$${i + 1}`).join(', ');

            const query = `INSERT INTO "${tableName}" (${quotedColumns})
                           VALUES (${placeholders})`;

            for (const row of rows) {
                const values = hdrs.map(h => {
                    if (h === 'Date') return fixDate(row[h]);
                    // столбцы, которые должны быть числами → мы их очистим
                    if (!isNaN(row[h])) return fixNumber(row[h]);

                    return row[h] === '' ? null : row[h];
                });
                await pool.query(query, values);
            }
            console.log('Все загружено:', tableName);
            await pool.end();
        });
}

loadData().catch(console.error);
