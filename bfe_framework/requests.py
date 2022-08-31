class Requests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    class GetRequests:

        @staticmethod
        def get_request_params(environ):
            # получаем параметры запроса
            query_string = environ['QUERY_STRING']
            # превращаем параметры в словарь
            request_params = Requests.parse_input_data(query_string)
            return request_params

    class PostRequests:

        @staticmethod
        def get_wsgi_input_data(env) -> bytes:
            # получаем длину тела
            content_length_data = env.get('CONTENT_LENGTH')
            print(f'длина - {type(content_length_data)}')
            content_length = int(content_length_data) if content_length_data else 0
            print(content_length)

            data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
            return data

        def parse_wsgi_input_data(self, data: bytes) -> dict:
            result = {}
            if data:
                # декодируем данные
                data_str = data.decode(encoding='utf-8')
                print(f'строка после декодирования - {data_str}')
                # собираем их в словарь
                result = Requests.parse_input_data(data_str)
            return result

        def get_request_params(self, environ):
            # получаем данные
            data = self.get_wsgi_input_data(environ)
            # превращаем данные в словарь
            data = self.parse_wsgi_input_data(data)
            return data
