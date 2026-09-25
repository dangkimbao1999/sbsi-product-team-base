import { expect, test } from "bun:test";
import { parseCsv, toTestCases } from "./uat-sheet";

const header = [
  ",,KỊCH BẢN KIỂM THỬ *,,,,,",
  "Mã trường hợp kiểm thử,Mục đích kiểm thử,Các bước thực hiện,Kết quả mong muốn,Kết quả thực tế,NGHIỆP VỤ,,",
  ",,,,,Kết quả hiện tại,PIC Nghiệp vụ,Ghi chú",
  ",Phân hệ Xác thực & Bảo mật,,,,,,",
];

test("parseCsv handles quoted newlines, commas and escaped quotes", () => {
  expect(parseCsv('a,"b\nc","say ""hi"", ok"\r\nd,e,f\n')).toEqual([
    ["a", "b\nc", 'say "hi", ok'],
    ["d", "e", "f"],
  ]);
});

test("toTestCases maps columns and keeps the real sheet row number", () => {
  const csv = [
    ...header,
    'TC_WEB_UC01_001,Đăng nhập,"Bước 1\nBước 2",OK,,Pass,BaoDK,note',
    "TC_WEB_UC01_002,Sai mật khẩu,B,Lỗi,,Untest,LongNH,",
  ].join("\n");
  expect(toTestCases(parseCsv(csv))).toEqual([
    { sheetRow: 5, id: "TC_WEB_UC01_001", purpose: "Đăng nhập", steps: "Bước 1\nBước 2", expected: "OK", actual: "", status: "Pass", pic: "BaoDK", note: "note" },
    { sheetRow: 6, id: "TC_WEB_UC01_002", purpose: "Sai mật khẩu", steps: "B", expected: "Lỗi", actual: "", status: "Untest", pic: "LongNH", note: "" },
  ]);
});

test("toTestCases throws when the column layout changed", () => {
  const moved = [header[0], header[1], ",,,,,PIC Nghiệp vụ,Kết quả hiện tại,Ghi chú"].join("\n");
  expect(() => toTestCases(parseCsv(moved))).toThrow(/layout/);
});
