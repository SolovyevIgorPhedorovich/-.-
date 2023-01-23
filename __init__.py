import RPi
import time
import DHT11
import post

#Результат датчика DHT11, метод DHT11.read()
class DHT11Result:

    ERR_NO_ERROR = 0
    ОШИБКА_MISSING_DATA = 1
    ERR_CRC = 2

    error_code = ERR_NO_ERROR
    temperature = -1
    humidity = -1

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = DHT11.T
        self.humidity = DHT11.H

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR

#Считывателя датчиков DHT11
class DHT11:

    __pin = 0

    def __init__(self, pin):
        self.__pin = pin

    def read(self):
        RPi.GPIO.setup(self.__pin, RPi.GPIO.OUT)

        # отправить начальный максимум
        self.__send_and_sleep(RPi.GPIO.HIGH, 0.05)

        # уменьшите до минимума
        self.__send_and_sleep(RPi.GPIO.LOW, 0.02)

        # изменить ввод с помощью подтягивания
        RPi.GPIO.setup(self.__pin, RPi.GPIO.IN, RPi.GPIO.PUD_UP)

        # собирать данные в массив
        data = self.__collect_input__collect_input()

        # анализировать длины всех периодов извлечения данных
        pull_up_lengths = self.__parse_data_pull_up_lengths__parse_data_pull_up_lengths(data)

        # если количество битов не совпадает, возвращается ошибка (4 байта данных + 1 байт контрольной суммы)
        if len(pull_up_lengths) != 40:
            return (DHT11Result.ERR_MISSING_DATA, 0, 0)

        # вычислять биты из длин периодов подтягивания
        bits = self.__calculate_bits(pull_up_lengths)

        # у нас есть биты, вычисляем байты
        the_bytes = self.__bits_to_bytes(bits)

        # вычислить контрольную сумму и проверить
        checksum = self.__calculate_checksum(the_bytes)
        if the_bytes[4] != checksum:
            return DHT11Result(DHT11Result.ERR_CRC, 0, 0)

        # Значение возвращаемых значений датчика
        # the_bytes[0]: значение влажности
        # the_bytes[1]: десятичная влажность
        # the_bytes[2]: значение температуры
        # the_bytes[3]: десятичная температура

        temperature = the_bytes[2] + float(the_bytes[3]) / 10
        humidity = the_bytes[0] + float(the_bytes[1]) / 10

        return DHT11Result(DHT11Result.ERR_NO_ERROR, temperature, humidity)

    def __send_and_sleep(self, output, sleep):
        RPi.GPIO.output(self.__pin, output)
        time.sleep(sleep)

    def __collect_input(self):
        # собирать данные, пока они не найдены
        unchanged_count = 0

        # это используется для определения того, где находится конец данных
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            current = RPi.GPIO.input(self.__pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break

        return data

    def __parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5

        state = STATE_INIT_PULL_DOWN

        lengths = [] # будет содержать длины периодов извлечения данных
        current_length = 0 # будет содержать длину предыдущего периода

        for i in range(len(data)):

            current = data[i]
            current_length += 1

            if state == STATE_INIT_PULL_DOWN:
                if current == RPi.GPIO.LOW:

                    # начальный откат
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == RPi.GPIO.HIGH:

                    # начальное подтягивание
                    state = STATE_DATA_FIRST_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_FIRST_PULL_DOWN:
                if current == RPi.GPIO.LOW:

                    # начальный вывод данных, следующим будет вывод данных
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_UP:
                if current == RPi.GPIO.HIGH:

                    # проверка подтягивания, равно ли оно 0 или 1
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN
                    continue
                else:
                    continue
            if state == STATE_DATA_PULL_DOWN:
                if current == RPi.GPIO.LOW:

                    # сохраняем длину предыдущего периода подтягивания
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP
                    continue
                else:
                    continue

        return lengths

    def __calculate_bits(self, pull_up_lengths):

        # найти самый короткий и самый длинный период
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(pull_up_lengths)):
            length = pull_up_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length

        # проверка является ли период длинным или коротким
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(pull_up_lengths)):
            bit = False
            if pull_up_lengths[i] > halfway:
                bit = True
            bits.append(bit)

        return bits

    def __bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if ((i + 1) % 8 == 0):
                the_bytes.append(byte)
                byte = 0

        return the_bytes

    def __calculate_checksum(self, the_bytes):
        return the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3] & 255