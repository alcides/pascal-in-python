# encoding=utf-8
from __future__ import with_statement
from llvm.core import *
from llvm.passes import *
from llvm.ee import *
 
# ヘルパー関数
def new_str_const(val):
    '''新しい文字列定数を生成する'''
    global mod, int8_type
    str = mod.add_global_variable(Type.array(int8_type, len(val) + 1), "")
    str.initializer = Constant.stringz(val)
    return str
 
def gep_first(emit, val):
    '''配列の先頭アドレスを取得する'''
    global int_type
    return emit.gep(val, (int_zero, int_zero))
 
def int_const(val):
    '''整数定数値オブジェクトを生成する'''
    global int_type
    return Constant.int(int_type, val)
 
class new_block(object):
    '''制御構造を表すためのヘルパークラス'''
    def __init__(self, emit, fun, label):
        self.emit = emit
        self.block = fun.append_basic_block(label)
        self.post_block = fun.append_basic_block("__break__" + label)
 
    def __enter__(self):
        self.emit.branch(self.block)
        self.emit.position_at_end(self.block)
        return self.block, self.post_block
 
    def __exit__(self, *arg):
        self.emit.branch(self.post_block)
        self.emit.position_at_end(self.post_block)
 
class emit_if(new_block):
    '''制御構造を表すためのヘルパークラス'''
    count = 0
    def __init__(self, emit, fun, cond):
        new_block.__init__(self, emit, fun, "if_%d" % self.__class__.count)
        self.__class__.count += 1
        emit.cbranch(cond, self.block, self.post_block)
 
# よく使う型はあらかじめ取っておく
int_type = Type.int()
int8_type = Type.int(8)
int_zero = int_const(0)
 
# ----------------------------------------------------------------------------
# コード生成
# ----------------------------------------------------------------------------
 
# モジュールを定義
mod = Module.new("plus1")
# モジュールに外部関数「printf」を追加
printf = mod.add_function(
    Type.function(
        Type.void(),
        (Type.pointer(int8_type, 0),), 1), "printf")
 
# --- 関数 plus1() ---
# モジュールに関数「plus1」を追加
plus1_fun = mod.add_function(
    Type.function(Type.void(), (int_type,)), "plus1")
 
# インストラクションコードを送出する
emit = Builder.new(plus1_fun.append_basic_block("entry"))
emit.call(printf,
    (
        gep_first(emit, new_str_const("%s: %d\n")),
        gep_first(emit, new_str_const("test")),
        emit.mul(plus1_fun.args[0], int_const(2))
        )
    )
emit.ret_void()
 
# --- 関数 loop() ---
# モジュールに関数「loop」を追加
loop_fun = mod.add_function(
    Type.function(Type.void(), ()), "loop")
 
# インストラクションコードを送出する
emit = Builder.new(loop_fun.append_basic_block("entry"))
count_var = emit.alloca(int_type)
 
emit.store(int_zero, count_var)
with new_block(emit, loop_fun, "loop") as (loop, _break):
    with emit_if(emit, loop_fun,
            emit.icmp(IPRED_ULT, emit.load(count_var), int_const(10))):
        emit.call(plus1_fun,
            (
                emit.load(count_var),
                )
            )
        emit.store(emit.add(emit.load(count_var), int_const(1)), count_var)
        emit.branch(loop)
emit.ret_void()
 
# ----------------------------------------------------------------------------
# 最適化
# ----------------------------------------------------------------------------
mp = ModuleProvider.new(mod) 
print "BEFORE:", loop_fun
 
pm = PassManager.new()
pm.add(TargetData.new(''))
pm.add(PASS_FUNCTION_INLINING)
pm.run(mod)
 
fp = FunctionPassManager.new(mp)
fp.add(TargetData.new(''))
fp.add(PASS_BLOCK_PLACEMENT)
fp.add(PASS_INSTRUCTION_COMBINING)
fp.add(PASS_TAIL_CALL_ELIMINATION)
fp.add(PASS_AGGRESSIVE_DCE)
# fp.add(PASS_CFG_SIMPLIFICATION) # XXX: バグってる
fp.add(PASS_DEAD_INST_ELIMINATION)
fp.add(PASS_DEAD_CODE_ELIMINATION)
for fun in mod.functions:
    fp.run(fun)
 
print "AFTER:", loop_fun
 
# ----------------------------------------------------------------------------
# 実行
# ----------------------------------------------------------------------------
ee = ExecutionEngine.new(mp)
ee.run_function(loop_fun, ())