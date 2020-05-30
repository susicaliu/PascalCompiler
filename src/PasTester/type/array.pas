program test_array;
type
    arr_int = array [1..50] of integer;
    arr_bool = array [1..50] of boolean;
var i,a: integer;
    arri:arr_int;
    arrb:arr_bool;
    bool1:boolean;
begin
  a:=1;
  arri[0]:=1+a;
  arri[1]:=2+arri[0];
  bool1:=true;
  arrb[0]:=true;
  arrb[1]:=bool1;
end.