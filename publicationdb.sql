
USE publication3;

CREATE TABLE BAIBAO 
(MaSoBB char(200) Not null,
 SoTrang int not null,
 Ten char(200),
 TieuDe char(200), 
 TomTat char(200), 
 TuKhoa char(200), 
 FileBB char(200), 
 primary key (MaSoBB)); 


 CREATE TABLE TONGQUAN 
 (MaSoBB char(200) Not null, 
 SoTrang int Not null, 
 primary key (MaSoBB), 
 foreign key (MaSoBB) references BAIBAO(MaSoBB)); 
 

 CREATE TABLE PHANBIEN 
 (MaSoBB char(200) Not null, 
 ISBN char(200) Not null, 
 SoTrang int Not null, 
 NhaXB char(200), NamXB char(200), 
 Ten char(200), TenTacGia char(200), 
primary key(MaSoBB), unique(ISBN), foreign key (MaSoBB) references BAIBAO(MaSoBB)); 


 CREATE TABLE NGHIENCUU 
 (MaSoBB char(200) Not null, 
 SoTrang int Not null, 
 primary key (MaSoBB), 
 foreign key (MaSoBB) references BAIBAO(MaSoBB)); 
 

 CREATE TABLE SACH 
 (MaSo char(200) Not null, 
 Loai char(200), 
 TacGia char(200), 
 primary key(MaSo)); 
 

 CREATE TABLE BAIBAOXB 
 ( MaSoBBXB char(200) not null,
 TrangThai char(200) Not null, 
 ThoiGian char(200), 
 FileXB char(200), 
 primary key (MaSoBBXB),
 foreign key(MaSoBBXB) references BAIBAO(MaSoBB));
 

 CREATE TABLE NHAKHOAHOC 
 (MaSo char(200) Not null, 
 primary key (MaSo)); 
 

 CREATE TABLE BANBIENTAP 
 (MaSoBBT char(200) Not null, 
 primary key(MaSoBBT), 
 foreign key(MaSoBBT) references NHAKHOAHOC(MaSo)); 
 

 CREATE TABLE TACGIA 
 (MaSoTG char(200) Not null, 
 CoQuan char(200), DiaChi char(200), 
 Mail char(200), NgheNghiep char(200), 
 primary key(MaSoTG), 
 foreign key(MaSoTG) references NHAKHOAHOC(MaSo)); 
 

 CREATE TABLE NGUOIPHANBIEN (
 MaSoNPB char(200) Not null, 
 Sdt char(200), 
 Ten char(200), 
 KiNang char(200), 
 ChuyenMon char(200), 
 CoQuan char(200), 
 MailCoQuan char(200), 
 MailCaNhan char(200), 
 primary key(MaSoNPB), 
 foreign key(MaSoNPB) references NHAKHOAHOC(MaSo)); 
 
 CREATE TABLE LOGIN
 (MS char(200) not null,
 Users char(200) not null,
 Passwords char(200) not null,
 primary key(MS),
 foreign key(MS) references BANBIENTAP(MaSoBBT),
 foreign key(MS) references TACGIA(MaSoTG),
 foreign key(MS) references NGUOIPHANBIEN(MaSoNPB));
 

 CREATE TABLE TIEUCHIDANHGIA 
 (NoiDung char(200) Not null,
 primary key(NoiDung)); 
 
 
 CREATE TABLE MUCDANHGIA 
 (NoiDung char(200) Not null, 
 Diem char(200) Not null, 
 GhiChu char(200), 
 primary key (NoiDung,Diem), foreign key(NoiDung) references TIEUCHIDANHGIA(NoiDung)); 
 
 ALTER TABLE BAIBAO 
 ADD MaSoBBT char(200) Not null, 
 ADD MaSoTG char(200) Not null, 
 ADD foreign key(MaSoTG) references TACGIA(MaSoTG), 
 ADD foreign key(MaSoBBT) references BANBIENTAP(MaSoBBT); 
 
 AlTER TABLE BAIBAOXB ADD MaSoBB char(200) Not null, 
 ADD foreign key(MaSoBB) references BAIBAO(MaSoBB); 
 
ALTER TABLE SACH ADD MaSoBaiBao char(200) Not null, 
ADD foreign key(MaSoBaiBao) references PHANBIEN(MaSoBB); 

 CREATE TABLE VIETBAO (
 MaSoBB char(200) Not null, 
 MaSoTG char(200) Not null, primary key(MaSoBB, MaSoTG), 
 foreign key (MaSoBB) references BAIBAO(MaSoBB), 
 foreign key (MaSoTG) references TACGIA(MaSoTG)); 
 
 CREATE TABLE PHANBIENBAIBAO (
 MaSoBB char(200) Not null, 
 MaSoNPB char(200) Not null, primary key(MaSoBB,MaSoNPB), 
 foreign key(MaSoBB) references BAIBAO(MaSoBB), 
 foreign key(MaSoNPB) references NGUOIPHANBIEN(MaSoNPB)); 
 

 CREATE TABLE XUATBAN (
 MaSoBB char(200) Not null, 
 MaSoNPB char(200) Not null, 
 MaSoBBT char(200) Not null, 
 DOI char(200) Not null, 
 primary key(MaSoBB, MaSoNPB, MaSoBBT), 
 unique(DOI), 
 foreign key(MaSoBB) references BAIBAO(MaSoBB), 
 foreign key(MaSoNPB) references NGUOIPHANBIEN(MaSoNPB), 
 foreign key(MaSoBBT) references BANBIENTAP(MaSoBBT)); 
 
 
 CREATE TABLE DANHGIA (MaSoBB char(200) Not null, 
 MaSoNPB char(200) Not null, NoiDung char(200) Not null, 
 primary key(MaSoNPB, MaSoBB, NoiDung), 
 foreign key(MaSoBB) references BAIBAO(MaSoBB),
 foreign key(MaSoNPB) references NGUOIPHANBIEN(MaSoNPB),
 foreign key(NoiDung) references TIEUCHIDANHGIA(NoiDung)) ;
 

 insert into NHAKHOAHOC
 values ('BBT1');
  insert into NHAKHOAHOC
 values ('TG1');
  insert into NHAKHOAHOC
 values ('TG2');
insert into NHAKHOAHOC
 values ('NPB1');
 insert into NHAKHOAHOC
 values ('NPB2');
 
 insert into BANBIENTAP
 values ('BBT1');
 
 insert into NGUOIPHANBIEN
 value ('NPB1','123456789','A','nhan xet','dai hoc','ABC','ABC@gmail.com','A@gmail.com');
 insert into NGUOIPHANBIEN
 value ('NPB2','123456788','B','nhan xet','thac sy','XYZ','XYZ@gmail.com','B@gmail.com');

 insert into TACGIA
 value ('TG1','ABC','Tan Binh','ABC@gmail.com','nha bao');
 insert into TACGIA
 value ('TG2','BCB','Go Vap','BCD@gmail.com','nha bao');
set FOREIGN_KEY_CHECKS=0;
insert into LOGIN
 values ('BBT1','BBT1','123');
insert into LOGIN
 values ('TG1','TG1','123');
insert into LOGIN
 values ('TG2','TG2','123');
insert into LOGIN
 values ('NPB1','NPB1','123');
insert into LOGIN
 values ('NPB2','NPB2','123');
set FOREIGN_KEY_CHECKS=1;
use publication3;

create table CAPNHAT
(MSCapNhat char(200) ,
TenCapNhat char(200),
MaSoNPB char(200),
Diem char(200),
GhiChuBBT char(200),
GhiChuTG char(200),
TrangThai char(200),
KetQua char(200)
);

Alter table BAIBAO
add MaSoNPB char(200) ,
add GhiChuBBT char(200),
add GhiChuTG char(200),
add Diem char(200),
add TrangThai char(200),
add KetQua char(200);

set FOREIGN_KEY_CHECKS=0;
insert into TACGIA
 value ('TG3','BCX','Go Vap','BCD@gmail.com','nha bao');
 set FOREIGN_KEY_CHECKS=1;
insert into BAIBAO
values('TQ1','5','Dế mèn','Chương cuối','Cuộc sống của dế mèn','Dế mèn','Google drive','BBT1','TG1','','','','','','');
insert into BAIBAO
values('TQ2','9','Dế choắt','Chương 2','Cuộc sống của dế choắt','Dế choắt','Google drive','BBT1','TG1','','','','','','');
insert into BAIBAO
values('TQ3','7','Dế con','Chương 4','Cuộc sống của dế con','Dế con','Google drive','BBT1','TG1','','','','','','');
insert into BAIBAO
values('NC1','15','Cá voi','Chương 3','Cuộc sống của cá voi','Cá voi','Google drive','BBT1','TG2','','','','','','');
insert into BAIBAO
values('NC2','13','Cá mập','Chương 4','Cuộc sống của cá mập','Cá mập','Google drive','BBT1','TG2','','','','','','');
insert into BAIBAO
values('NC3','19','Cá đuối','Chương 3','Cuộc sống của cá đuối','Cá đuối','Google drive','BBT1','TG2','','','','','','');
insert into BAIBAO
values('PB1','3','Chim sâu','Chương 1','Cuộc sống của chim sâu','Chim sâu','Google drive','BBT1','TG3','','','','','','');
insert into BAIBAO
values('PB2','5','Dâu tây','Chương cuối','Cuộc sống của dâu tây','Dâu tây','Google drive','BBT1','TG3','','','','','','');
insert into BAIBAO
values('PB3','8','Quả táo','Chương 21','Cuộc sống của quả táo','Quả táo','Google drive','BBT1','TG3','','','','','','');
set FOREIGN_KEY_CHECKS=0;
insert into LOGIN
 values ('TG3','TG3','123');
set FOREIGN_KEY_CHECKS=1;
