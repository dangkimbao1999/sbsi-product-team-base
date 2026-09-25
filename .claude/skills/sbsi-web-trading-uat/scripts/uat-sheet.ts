// Read-only view of the SBSI Web Trading UAT Google Sheet (tab gid 581688525).
// Usage: bun uat-sheet.ts [--id TC_WEB_UC01_001] [--pic BaoDK] [--status Untest]
// Prints matching test cases as JSON, each with its real `sheetRow` for writing back.

const SHEET_ID = "1h7OFH0E7nySstbyY9ffyMYw350vT1hX_j0yX5hYmoBM";
const GID = "581688525";
const EXPORT_URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/export?format=csv&gid=${GID}`;

export type TestCase = {
  sheetRow: number;
  id: string;
  purpose: string;
  steps: string;
  expected: string;
  actual: string;
  status: string;
  pic: string;
  note: string;
};

export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (c !== "\r") field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows;
}

export function toTestCases(rows: string[][]): TestCase[] {
  const headerIdx = rows.findIndex((r) => r[0] === "Mã trường hợp kiểm thử");
  const sub = rows[headerIdx + 1] ?? [];
  if (headerIdx < 0 || rows[headerIdx][4] !== "Kết quả thực tế" || sub[5] !== "Kết quả hiện tại" || sub[6] !== "PIC Nghiệp vụ" || sub[7] !== "Ghi chú") {
    throw new Error("UAT sheet layout changed (expected A=Mã TC, E=Kết quả thực tế, F=Kết quả hiện tại, G=PIC Nghiệp vụ, H=Ghi chú) — update this script and SKILL.md before reading/writing");
  }
  return rows.flatMap((r, i) =>
    /^TC_WEB_/.test(r[0])
      ? [{ sheetRow: i + 1, id: r[0], purpose: r[1], steps: r[2], expected: r[3], actual: r[4], status: r[5], pic: r[6], note: r[7] }]
      : [],
  );
}

if (import.meta.main) {
  const args = process.argv.slice(2);
  const opt = (name: string) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const res = await fetch(EXPORT_URL);
  if (!res.ok || !res.headers.get("content-type")?.includes("text/csv")) {
    throw new Error(`Cannot export UAT sheet as CSV (HTTP ${res.status}, ${res.headers.get("content-type")}) — sheet may no longer be link-readable; ask the user`);
  }
  const id = opt("--id"), pic = opt("--pic"), status = opt("--status");
  const cases = toTestCases(parseCsv(await res.text())).filter(
    (t) => (!id || t.id === id) && (!pic || t.pic === pic) && (!status || t.status === status),
  );
  if (id && cases.length !== 1) throw new Error(`Expected exactly 1 row for ${id}, found ${cases.length}`);
  console.log(JSON.stringify(cases, null, 2));
}
