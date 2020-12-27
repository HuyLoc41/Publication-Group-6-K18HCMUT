use publication2;

DELIMITER $$
CREATE PROCEDURE CheckLogin(IN a char(200),IN b char(200))
BEGIN
SELECT * FROM LOGIN,BANBIENTAP WHERE Users = a AND Passwords = b AND LOGIN.MS=BANBIENTAP.MaSoBBT;
END;

DELIMITER $$
CREATE PROCEDURE UpdateBBT(IN a char(200),IN b char(200), IN c char(200),IN d char(200),IN e char(200))
BEGIN
UPDATE BAIBAO SET MaSoNPB= a,TrangThai= b, KetQua=c, NgayCapNhatKQ=d where MaSoBB=e;
END;

DELIMITER $$
CREATE PROCEDURE PhanLoai(IN a char(200),IN b char(200), IN c char(200),IN d char(200),IN e char(200))
BEGIN
SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.MaSoNPB="";
END;

DELIMITER $$
CREATE PROCEDURE PhanLoaiTheoNam(IN a char(200),IN b char(200))
BEGIN
SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.TrangThai="Đã đăng" AND BAIBAO.NgayGui >  DATE_SUB(a, INTERVAL 4 YEAR) AND BAIBAO.NgayGui <= b ;
END;

DELIMITER $$
CREATE PROCEDURE TimKiem(IN a char(200), IN b char(200))
BEGIN
SELECT * FROM BAIBAO WHERE BAIBAO.TrangThai=b AND BAIBAO.MaSoTG = a;
END;

DELIMITER $$
CREATE PROCEDURE Dem(IN a char(200))
BEGIN
SELECT COUNT(*) FROM BAIBAO WHERE BAIBAO.TrangThai=a;
END;

DELIMITER $$
CREATE PROCEDURE UpdateNPB(IN a char(200),IN b char(200),IN c char(200),IN d char(200),IN e char(200),IN f char(200),IN g char(200),IN h char(200))
BEGIN
UPDATE NGUOIPHANBIEN SET  Sdt =a, Ten =b, KiNang =c, ChuyenMon =d, CoQuan =e, MailCoQuan =f, MailCaNhan =g WHERE MaSoNPB =h;
END;

DELIMITER $$
CREATE PROCEDURE UpdateNPB1(IN a char(200),IN b char(200),IN c char(200),IN d char(200))
BEGIN
UPDATE BAIBAO SET Diem= a,GhiChuBBT= b, GhiChuTG=c where MaSoBB=d;
END;

DELIMITER $$
CREATE PROCEDURE UpdateNPB2(IN a char(200),IN b char(200),IN c char(200),IN d char(200))
BEGIN
UPDATE BAIBAO SET Diem= a,GhiChuBBT= b, GhiChuTG=c where MaSoBB=d;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB1(IN a char(200),IN b char(200))
BEGIN
SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)=a AND (BAIBAO.TrangThai="Phản biện" OR BAIBAO.TrangThai="Phản hồi phản biện") and BAIBAO.MaSoNPB=b;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB2(IN a char(200),IN b char(200),IN c char(200))
BEGIN
SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(a, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= b and BAIBAO.MaSoNPB=c;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB3(IN a char(200))
BEGIN
SELECT * FROM BAIBAO WHERE (BAIBAO.TrangThai="Phản biện" OR BAIBAO.TrangThai="Phản hồi phản biện") and BAIBAO.MaSoNPB=a ORDER BY MaSoTG;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB4(IN a char(200),IN b char(200),IN c char(200))
BEGIN
SELECT * FROM BAIBAO WHERE BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(a, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= b and BAIBAO.MaSoNPB=c ORDER BY MaSoTG;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB4(IN a char(200),IN b char(200),IN c char(200))
BEGIN
SELECT * FROM BAIBAO WHERE BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(a, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= b and BAIBAO.MaSoNPB=c ORDER BY MaSoTG;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB5(IN a char(200) )
BEGIN
SELECT * FROM BAIBAO WHERE BAIBAO.KetQua="acceptance" and MaSoNPB=a;
END;

DELIMITER $$
CREATE PROCEDURE TimKiemNPB6(IN a char(200) )
BEGIN
SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2020-01-01" and NgayCapNhatKQ<"2021-01-01" and MaSoNPB=a;
END;

DELIMITER $$
CREATE PROCEDURE UpdateTG(IN a char(200),IN b char(200),IN c char(200),IN d char(200),IN e char(200) )
BEGIN
UPDATE TACGIALL SET  CoQuan =a, DiaChi =b, Mail =c, NgheNghiep =d WHERE MaSoTGLL =e ;
END;

DELIMITER $$
CREATE PROCEDURE UpdateTG1(IN a char(200),IN b char(200),IN c char(200),IN d char(200),IN e char(200),IN f char(200),IN g char(200),IN h char(200) )
BEGIN
UPDATE BAIBAO SET MaSoTG =a, SoTrang =b, TieuDe =c, Ten =d, TomTat=e,TuKhoa=f,FileBB=g WHERE MaSoBB = h ;
END;

DELIMITER $$
CREATE PROCEDURE UpdateTG1(IN a char(200),IN b char(200),IN c char(200),IN d char(200),IN e char(200),IN f char(200),IN g char(200),IN h char(200) )
BEGIN
UPDATE BAIBAO SET MaSoTG =a, SoTrang =b, TieuDe =c, Ten =d, TomTat=e,TuKhoa=f,FileBB=g WHERE MaSoBB = h ;
END;

DELIMITER $$
CREATE PROCEDURE SelectTG1(IN a char(200) )
BEGIN
SELECT * from TACGIA where MaSoTG=(SELECT MaSoTG from BAIBAO where MaSoBB=a);
END;

DELIMITER $$
CREATE PROCEDURE SelectTG2(IN a char(200),IN b char(200) )
BEGIN
SELECT * from BAIBAO where a=b;
END;

DELIMITER $$
CREATE PROCEDURE SelectTG4(IN a char(200))
BEGIN
SELECT * from BAIBAO where TrangThai="Đã đăng" AND SUBSTRING(NgayCapNhatKQ, 1, 4)=a;
END;

DELIMITER $$
CREATE PROCEDURE CountTG5(IN a char(200))
BEGIN
SELECT COUNT(*) from BAIBAO where ((SELECT convert(a, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=0);
END;

DELIMITER $$
CREATE PROCEDURE CountTG6(IN a char(200),IN b char(200))
BEGIN
SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)=a AND TrangThai="Đã đăng" AND ((SELECT convert(b, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=0);
END;






