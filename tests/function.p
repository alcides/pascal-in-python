program test3; 
var 
	A : integer; 

	procedure ScopeInner; 
	var A : integer; 
		begin
		A := 10; 
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
	ScopeInner;
	
	writeint(A); 
end.
