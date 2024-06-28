# 変数配列の作成
from amplify import VariableGenerator
gen = VariableGenerator()
q = gen.array("Binary", 2)
print(q)

# 目的関数の作成
f = q[0] * q[1] + q[0] -q[1] + 1
print(f)

from amplify import FixstarsClient
client = FixstarsClient()
client.token = "AE/VfQDHqAtq9NOTUnJyxWiDTSGa7avMJQe" 
client.parameters.timeout = 1000
from amplify import solve
result = solve(f, client)

print(result.best.values)
print(result.best.objective)
print(f"{q} = {q.evaluate(result.best.values)}")