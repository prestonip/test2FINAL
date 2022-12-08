# test2FINAL
Preston's OFFICIAL PLC Test2 resubmission repo! :)


'''
S' -> YOINKY <stmt> SPLOINKY
<stmt> -> <var_stmt>
<stmt> -> <select_stmt>
<stmt> -> <loop_stmt>
<stmt> -> <block>
<var_stmt> -> id
<var_stmt> -> id = <expr>
<select_stmt> ->  maybe ( <bool_expr> ) <stmt> 
<select_stmt> ->  maybe ( <bool_expr> ) <stmt> actually <block>
<loop_stmt> ->  loop ( <bool_expr> ) <block> 
<block> -> { <stmt> ; }
<block> -> { }
<expr> -> <term> 
<expr> -> <term> * <term>
<expr> -> <term> - <term>
<term> -> <factor> 
<term> -> <factor> + <factor>
<term> -> <factor> / <factor>
<term> -> <factor> % <factor>
<factor> -> id
<factor> -> int_lit
<factor> -> ( <expr> )

<bool_inc> -> <bool_eval>
<bool_inc> -> <bool_eval> and <bool_eval>
<bool_inc> -> <bool_eval> or <bool_eval>
<bool_eval> -> <bool_expr>
<bool_eval> -> <bool_expr> != <bool_expr>
<bool_eval> -> <bool_expr> == <bool_expr>
<bool_eval> -> <bool_expr> >= <bool_expr>
<bool_eval> -> <bool_expr> <= <bool_expr>
<bool_eval> -> <bool_expr> < <bool_expr>
<bool_eval> -> <bool_expr> > <bool_expr>
<bool_expr> -> <bool_term> 
<bool_expr> -> <bool_term> * <bool_term>
<bool_expr> -> <bool_term> - <bool_term>
<bool_term> -> <bool_factor>
<bool_term> -> <bool_factor> + <bool_factor>
<bool_term> -> <bool_factor> / <bool_factor>
<bool_term> -> <bool_factor> % <bool_factor>
<bool_factor> -> id 
<bool_factor> -> int_lit 
<bool_factor> -> bool_lit
'''

This grammar conforms to the rules of an LL grammar. There is no lefthand recursion, and no rule ever calls itself.

Also, * and + are swapped in the syntax rules. The two tokens retian their conventional meanings (multiplication and addition, respectively), and thusly break the PEMDAS precedence rule.
