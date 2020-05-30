program test_1;
type
    arr = array [1..50] of integer;
var i,a: integer;
    f:arr;

function fib(x:integer):integer;
begin
  fib:=fib(x - 2) + fib(x - 1);
end;

begin
  for i:=1 to 7 do begin
    f[i]:=fib(i);
  end;
end.