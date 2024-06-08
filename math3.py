from random import randint, uniform
import sqlite3


class MyMath:
    def generate_square_x(self):
        '''Вернет кв уравнение в строковом формате'''
        self.a_sq = randint(-3, 5)
        if self.a_sq == 0:
            while self.a_sq == 0:
                self.a_sq = randint(-3, 5)
        self.b_sq = randint(-11, 11)
        self.c_sq = randint(-11, 11)
        if self.b_sq == 0:
            self.b_sq = 1
        elif self.c_sq == 0:
            self.c_sq = 1

        if self.b_sq == 1:
            if self.c_sq < 0:
                return f'{self.a_sq}x\u00B2 + x - {-self.c_sq} = 0'
            else:
                return f'{self.a_sq}x\u00B2 + x + {self.c_sq} = 0'

        elif self.b_sq == -1:
            if self.c_sq < 0:
                return f'{self.a_sq}x\u00B2 - x - {-self.c_sq} = 0'
            else:
                return f'{self.a_sq}x\u00B2 - x + {self.c_sq} = 0'

        if self.b_sq < 0 and self.c_sq > 0:
            sq_x = f'{self.a_sq}x\u00B2 - {-self.b_sq}x + {self.c_sq} = 0'
        elif self.b_sq > 0 and self.c_sq < 0:
            sq_x = f'{self.a_sq}x\u00B2 + {self.b_sq}x - {-self.c_sq} = 0'
        elif self.b_sq < 0 and self.c_sq < 0:
            sq_x = f'{self.a_sq}x\u00B2 - {-self.b_sq}x - {-self.c_sq} = 0'
        else:
            sq_x = f'{self.a_sq}x\u00B2 + {self.b_sq}x + {self.c_sq} = 0'

        if self.a_sq == 1:
            sq_x = sq_x[1:]
        elif self.a_sq == -1:
            sq_x = f'-{sq_x[2:]}'
        return sq_x

    def answer_square_x(self):
        """
        Вернет 1) если дискриминант положительный - список из 2 целых или дробных чисел
                  2) если дискриминант 0 - одно целое или дробное число
                  3) если дискриминант отрицательный - строку "Корней нет"
           корни последнего сгенерированного кв уравнения
           """
        d = (abs(self.b_sq) ** 2) - (4 * self.a_sq * self.c_sq)
        if d == 0:
            self.answer = (-self.b_sq) / (2 * self.a_sq)
            return self.answer

        elif d > 0:
            x1 = (-self.b_sq - d ** 0.5) / (2 * self.a_sq)
            x2 = (-self.b_sq + d ** 0.5) / (2 * self.a_sq)
            if isinstance(x1, int) and not isinstance(x2, int):
                self.answer = sorted([x1, round(x2, 2)])
            elif isinstance(x2, int) and not isinstance(x1, int):
                self.answer = sorted([round(x1, 2), x2])
            elif isinstance(x1, int) and isinstance(x2, int):
                self.answer = sorted([x1, x2])
            elif not isinstance(x1, int) and not isinstance(x2, int):
                self.answer = sorted([round(x1, 2), round(x2, 2)])
            return self.answer

        else:
            self.answer = 'Корней нет'
            return self.answer

    def check_answer_square_x(self, user_answer):
        """
        В качестве ответа может быть принято
        1) 2 корня кв уравнения через пробел(это могут быть целые числа или дробные(округлите до сотых) числа)
        2) один корень - целое чило или дробное(округлите до сотых) число
        3) строка 'Корней нет'
        """
        if user_answer == 'Корней нет':
            if str(self.answer_square_x()) == user_answer:
                return 'Верно'
            else:
                return f'Неверно. Правильный ответ {self.answer_square_x()}.'

        elif isinstance(user_answer, int) or isinstance(user_answer, float):
            if float(user_answer) == float(self.answer_square_x()):
                return 'Верно'
            else:
                return f'Неверно. Правильный ответ {self.answer_square_x()}.'

        temp = [float(i) for i in user_answer.split(' ')]
        if sorted(temp) == list(self.answer_square_x()):
            return ['Верно', True, 'square_x']
        else:
            return [f'Неверно. Правильный ответ {self.answer_square_x()}.', False]

    def generate_line_x(self):
        """
        Вернет линейное уравнение в строковом формате
        """
        self.a_li = randint(-11, 11)
        self.b_li = randint(-11, 11)
        self.c_li = randint(-11, 11)

        if self.b_li < 0:
            line_x = f'{self.a_li}x - {-self.b_li} = {self.c_li}'
        elif self.b_li > 0:
            line_x = f'{self.a_li}x + {self.b_li} = {self.c_li}'
        elif self.b_li == 0:
            self.b_li = 1
            line_x = f'{self.a_li}x + {self.b_li} = {self.c_li}'

        if self.a_li == 1 or self.a_li == 0:
            self.a_li = 1
            line_x = line_x[1:]
        elif self.a_li == -1:
            line_x = f'-{line_x[2:]}'
        return line_x

    def answer_line_x(self):
        """
        Вернет корень последнего сгенерированного линейного уравнения
        """
        temp = self.c_li + (-self.b_li)
        if temp / self.a_li == temp // self.a_li:
            self.x = temp // self.a_li
        else:
            self.x = round(temp / self.a_li, 2)
        return self.x

    def check_answer_line_x(self, user_answer):
        """
        В качестве ответа может быть принято
        целое число или дробное(округлите до сотых) число
        """
        if float(user_answer) == float(self.answer_line_x()):
            return ['Верно', True, 'line_x']
        else:
            return [f'Неверно. Правильный ответ {self.answer_line_x()}.', False]

    def generate_sum_stage_1(self):
        """
        Вернет пример на сложение простого уровня сложности в строковом формате
        """
        self.a_s_1 = randint(1, 101)
        self.b_s_1 = randint(1, 101)
        return f'{self.a_s_1} + {self.b_s_1} = ?'

    def answer_sum_stage_1(self):
        """
        Вернет решение последнего сгенерированного примера на сложение простого уровня сложности
        """
        return self.a_s_1 + self.b_s_1

    def check_answer_sum_stage_1(self, user_answer):
        """
        Проверит ответ пользователя на пример на сложение простого уровня сложности
        """
        if float(self.answer_sum_stage_1()) == float(user_answer):
            return ['Верно', True, 's_1']
        else:
            return [f'Неверно. Правильный ответ {self.answer_sum_stage_1()}.', False]

    def generate_sum_stage_2(self):
        """
        Вернет пример на сложение среднего уровня сложности в строковом формате
        """
        self.a_s_2 = round(uniform(1, 20), 2)
        self.b_s_2 = round(uniform(1, 20), 2)
        return f'{self.a_s_2} + {self.b_s_2} = ?'

    def answer_sum_stage_2(self):
        """
        Вернет ответ на последний сгенерированный пример на сложение среднего уровня сложности
        """
        return self.a_s_2 + self.b_s_2

    def check_answer_sum_stage_2(self, user_answer):
        """
        Проверит ответ пользователя на последний сгенерированный пример на сложение среднего уровня сложности
        """
        if float(user_answer) == float(self.answer_sum_stage_2()):
            return ['Верно', True, 's_2']
        else:
            return [f'Неверно. Правильный ответ {self.answer_sum_stage_2()}.', False]

    def generate_sum_stage_3(self):
        """
        Вернет пример на сложение высокого уровня сложности в строковом формате
        """
        self.a_s_3 = randint(1, 30)
        self.b_s_3 = round(uniform(1, 30), 2)
        self.c_s_3 = round(uniform(1, 30), 2)
        self.d_s_3 = randint(1, 30)
        return f'{self.a_s_3} + {self.b_s_3} + {self.c_s_3} + {self.d_s_3} = ?'

    def answer_sum_stage_3(self):
        """
        Вернет ответ на последний сгенерированный пример на сложение высокого уровня сложности
        """
        return self.a_s_3 + self.b_s_3 + self.c_s_3 + self.d_s_3

    def check_answer_sum_stage_3(self, user_answer):
        """
        Проверил ответ пользователя на пример на сложение высокого уровня сложности
        """
        if float(user_answer) == float(self.answer_sum_stage_3()):
            return ['Верно', True, 's_3']
        else:
            return [f'Неверно. Правильный ответ {self.answer_sum_stage_3()}.', False]

    def generate_min_stage_1(self):
        """
        Вернет пример на вычитание простого уровня сложности в строковом формате
        """
        self.a_m_1 = randint(1, 101)
        self.b_m_1 = randint(1, 101)
        return f'{self.a_m_1} - {self.b_m_1} = ?'

    def answer_min_stage_1(self):
        """
        Вернет решение последнего сгенерированного примера на вычитание простого уровня сложности
        """
        return self.a_m_1 - self.b_m_1

    def check_answer_min_stage_1(self, user_answer):
        """
        Проверит ответ пользователя на пример на вычитание простого уровня сложности
        """
        if float(self.answer_min_stage_1()) == float(user_answer):
            return ['Верно', True, 'm_1']
        else:
            return [f'Неверно. Правильный ответ {self.answer_min_stage_1()}.', False]

    def generate_min_stage_2(self):
        """
        Вернет пример на вычитание среднего уровня сложности в строковом формате
        """
        self.a_m_2 = round(uniform(1, 20), 2)
        self.b_m_2 = round(uniform(1, 20), 2)
        return f'{self.a_m_2} - {self.b_m_2} = ?'

    def answer_min_stage_2(self):
        """
        Вернет ответ на последний сгенерированный пример на вычитание среднего уровня сложности
        """
        return round(self.a_m_2 - self.b_m_2, 2)

    def check_answer_min_stage_2(self, user_answer):
        """
        Проверит ответ пользователя на пример на вычитание среднего уровня сложности
        """
        if float(user_answer) == float(self.answer_min_stage_2()):
            return ['Верно', True, 'm_2']
        else:
            return [f'Неверно. Правильный ответ {self.answer_min_stage_2()}', False]

    def generate_min_stage_3(self):
        """
        Вернет пример на вычитание высокого уровня сложности в строковом формате
        """
        self.a_m_3 = randint(1, 30)
        self.b_m_3 = round(uniform(1, 30), 2)
        self.c_m_3 = round(uniform(1, 30), 2)
        self.d_m_3 = randint(1, 30)
        return f'{self.a_m_3} - {self.b_m_3} - {self.c_m_3} - {self.d_m_3} = ?'

    def answer_min_stage_3(self):
        """
        Вернет ответ на последний сгенерированный пример на вычитание высокого уровня сложности
        """
        return round(self.a_m_3 - self.b_m_3 - self.c_m_3 - self.d_m_3, 2)

    def check_answer_min_stage_3(self, user_answer):
        """
        Проверит ответ пользователя на пример на вычитание высокого уровня сложности
        """
        if float(user_answer) == float(self.answer_min_stage_3()):
            return ['Верно', True, 'm_3']
        else:
            return [f'Неверно. Правильный ответ {self.answer_min_stage_3}.', False]

    def generate_crop_stage_1(self):
        """
        Вернет пример на деление в строковом формате
        """
        self.a_cr_1 = randint(1, 51)
        self.b_cr_1 = randint(1, 51)
        return f'{self.a_cr_1} : {self.b_cr_1} = ?'

    def answer_crop_stage_1(self):
        """
        Вернет решение последнего сгенерированного примера на деление
        """
        if self.a_cr_1 / self.b_cr_1 == self.a_cr_1 // self.b_cr_1:
            return self.a_cr_1 // self.b_cr_1
        else:
            return round(self.a_cr_1 / self.b_cr_1, 2)

    def check_answer_crop_stage_1(self, user_answer):
        """
        Проверит ответ пользователя на пример на деление простого уровня сложности
        """
        if float(self.answer_crop_stage_1()) == float(user_answer):
            return ['Верно', True, 'cr_1']
        else:
            return [f'Неверно. Правильный ответ {self.answer_crop_stage_1()}.', False]

    def generate_crop_stage_2(self):
        """
        Вернет пример на деление среднего уровня сложности в строковом формате
        """
        self.a_cr_2 = round(uniform(1, 20), 2)
        self.b_cr_2 = round(uniform(1, 20), 2)
        return f'{self.a_cr_2} : {self.b_cr_2} = ?'

    def answer_crop_stage_2(self):
        """
        Вернет ответ на последний сгенерированный пример на деление среднего уровня сложности
        """
        return round(self.a_cr_2 / self.b_cr_2, 2)

    def check_answer_crop_stage_2(self, user_answer):
        """
        Проверит ответ пользователя на пример на деление среднего уровня сложности
        """
        if float(user_answer) == float(self.answer_crop_stage_2()):
            return ['Верно', True, 'cr_2']
        else:
            return [f'Неверно. Правильный ответ {self.answer_crop_stage_2()}.', False]

    def generate_crop_stage_3(self):
        """
        Вернет пример на деление высокого уровня сложности в строковом формате
        :return:
        """
        self.a_cr_3 = randint(1, 30)
        self.b_cr_3 = round(uniform(1, 30), 2)
        self.c_cr_3 = round(uniform(1, 30), 2)
        self.d_cr_3 = randint(1, 30)
        return f'({self.a_cr_3} : {self.b_cr_3}) : ({self.c_cr_3} : {self.d_cr_3}) = ?'

    def answer_crop_stage_3(self):
        """
        Вернет ответ на последний сгенерированный пример на деление высокого уровня сложности
        """
        temp1 = self.a_cr_3 / self.b_cr_3
        temp2 = self.c_cr_3 / self.d_cr_3
        return round(temp1 / temp2, 2)

    def check_answer_crop_stage_3(self, user_answer):
        """
        Проверит ответ пользователя на пример на деление высокого уровня сложности
        """
        if float(user_answer) == float(self.answer_crop_stage_3()):
            return ['Верно', True, 'cr_3']
        else:
            return [f'Неверно. Правильный ответ {self.answer_crop_stage_3()}', False]

    def generate_multiply_stage_1(self):
        """
        Вернет пример на умножение в строковом формате
        """
        self.a_mul_1 = randint(1, 21)
        self.b_mul_1 = randint(1, 21)
        return f'{self.a_mul_1} * {self.b_mul_1} = ?'

    def answer_multiply_stage_1(self):
        """
        Вернет решение последнего сгенерированного примера на умножение
        """
        return self.a_mul_1 * self.b_mul_1

    def check_answer_multiply_stage_1(self, user_answer):
        """
        Проверит ответ пользователя на пример на умножение простого уровня сложности
        """
        if float(self.answer_multiply_stage_1()) == float(user_answer):
            return ['Верно', True, 'mul_1']
        else:
            return [f'Неверно. Правильный ответ {self.answer_multiply_stage_1()}.', False]

    def generate_multiply_stage_2(self):
        """
        Вернет пример на умножение среднего уровня сложности в строковом формате
        """
        self.a_mul_2 = round(uniform(1, 10), 2)
        self.b_mul_2 = round(uniform(1, 10), 2)
        return f'{self.a_mul_2} * {self.b_mul_2} = ?'

    def answer_multiply_stage_2(self):
        """
        Вернет ответ на последний сгенерированный пример на умножение среднего уровня сложности
        """
        return round(self.a_mul_2 * self.b_mul_2, 2)

    def check_answer_multiply_stage_2(self, user_answer):
        """
        Проверит ответ пользователя на пример на умножение среднего уровня сложности
        """
        if float(user_answer) == float(self.answer_multiply_stage_2()):
            return ['Верно', True, 'mul_2']
        else:
            return [f'Неверно. Правильный ответ {self.answer_multiply_stage_2()}', False]

    def generate_multiply_stage_3(self):
        """
        Вернет пример на умножение высокого уровня сложности в строковом формате
        """
        self.a_mul_3 = randint(1, 10)
        self.b_mul_3 = round(uniform(1, 10), 2)
        self.c_mul_3 = round(uniform(1, 10), 2)
        self.d_mul_3 = randint(1, 10)
        return f'({self.a_mul_3} * {self.b_mul_3}) * ({self.c_mul_3} * {self.d_mul_3}) = ?'

    def answer_multiply_stage_3(self):
        """
        Вернет ответ на последний сгенерированный пример на умножение высокого уровня сложности
        """
        return round((self.a_mul_3 * self.b_mul_3) * (self.c_mul_3 * self.d_mul_3), 2)

    def check_answer_multiply_stage_3(self, user_answer):
        """
        Проверит ответ пользователя на пример на умножение высокого уровня сложности
        """
        if float(user_answer) == float(self.answer_multiply_stage_3()):
            return ['Верно', True, 'mul_3']
        else:
            return [f'Неверно. Правильный ответ {self.answer_multiply_stage_3()}', False]

    def edit_rating(self, login, true_task):
        data = {'square_x': 15, 'line_x': 10, 's_1': 3, 's_2': 5, 's_3': 10,
                'm_1': 3, 'm_2': 5, 'm_3': 10, 'cr_1': 3, 'cr_2': 5,
                'cr_3': 10, 'mul_1': 3, 'mul_2': 5, 'mul_3': 10}
        point = data[true_task]
        con = sqlite3.connect('project.db')
        cursor = con.cursor()
        points = cursor.execute(f'''SELECT points FROM stats WHERE login="{login}"''').fetchone()
        if not points:
            points = point
        else:
            print(points)
            points = point + points[0]
        print(points)
        cursor.execute(f'''UPDATE stats SET points={points}  WHERE login="{login}"''')
        con.commit()
        con.close()
        return point