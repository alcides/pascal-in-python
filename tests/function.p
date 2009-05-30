program test3; 
var 
	A : integer; 

	procedure ScopeInner(num : integer); 
	var A : integer; 
		begin
		A := 10 + num; 
		writeint(A) 
	end; 

{	function Summation(num : integer) : integer;
	begin
		if num = 1 then 
			Summation := 1 
		else 
			Summation := Summation(num-1) + num 
	end; 
}
begin 
	A := 20; 
	writeint(A); 
	ScopeInner(A);
	
	writeint(A); 
end.
