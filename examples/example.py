class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        return a + b

    def multiply(self, x, y):
        return x * y

    def calculate_expression(self, expression):
        # 这是一个计算表达式的示例
        numbers = [1, 2, 3, 4, 5]
        total = sum(numbers)
        return total

# 使用示例
calc = Calculator()
result1 = calc.add(10, 20)
result2 = calc.multiply(5, 6)
result3 = calc.calculate_expression("1+2+3")
