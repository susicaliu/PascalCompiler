program test_2;
type
    arr = array [1..50] of integer;
var i,a,b,c,s: integer;
    f:arr;

function g1(x:integer):integer;
  var s:integer;
  function g2(x:integer):integer;
    var s:integer;
    begin
        s:=2;
        g2:=1;
    end;
  begin
    s:=1;
    g2(12);
    g1:=1;
  end;

begin
  s:=0;
  g1(3);
end.
