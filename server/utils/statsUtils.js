function isNumeric(val) {
  if (val === null || val === undefined || val === '') return false;
  return !isNaN(parseFloat(val)) && isFinite(val);
}

function isDate(val) {
  if (val === null || val === undefined || val === '') return false;
  const d = new Date(val);
  return !isNaN(d.getTime()) && isNaN(Number(val));
}

function detectType(values) {
  const nonEmpty = values.filter((v) => v !== null && v !== undefined && v !== '');
  if (nonEmpty.length === 0) return 'categorical';
  const numericCount = nonEmpty.filter(isNumeric).length;
  const dateCount = nonEmpty.filter(isDate).length;
  if (numericCount / nonEmpty.length > 0.8) return 'numeric';
  if (dateCount / nonEmpty.length > 0.8) return 'date';
  return 'categorical';
}

function computeStats(rows) {
  if (!rows || rows.length === 0) return [];
  const columnNames = Object.keys(rows[0]);
  return columnNames.map((name) => {
    const values = rows.map((r) => r[name]);
    const nullCount = values.filter((v) => v === null || v === undefined || v === '').length;
    const nonEmpty = values.filter((v) => v !== null && v !== undefined && v !== '');
    const uniqueCount = new Set(nonEmpty).size;
    const type = detectType(values);

    let min = null, max = null, mean = null;
    if (type === 'numeric') {
      const nums = nonEmpty.map(Number);
      min = Math.min(...nums);
      max = Math.max(...nums);
      mean = nums.reduce((a, b) => a + b, 0) / nums.length;
      mean = Math.round(mean * 100) / 100;
    }

    return { name, type, nullCount, uniqueCount, min, max, mean };
  });
}

module.exports = { computeStats };
