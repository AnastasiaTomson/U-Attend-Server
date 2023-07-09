# U-Attend

<hr>


<span style="color: #ff9243">**Наша команда**</span>

- Жмурко Анастасия Дмитриевна
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [VK @anastasia.tomson](https://vk.com/anastasia.tomson)
- Сапрыкина Алина Александровна &nbsp;&nbsp;&nbsp;&nbsp;[VK @aernika](https://vk.com/aernika)
- Галсанов Булат Мункуевич
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[VK @disc1ple](https://vk.com/disc1ple)

<span style="color: #ff9243">**Описание**</span><br>

<b>U-Attend</b> — приложение для контроля посещаемости в Сибирском Федеральном Университете.

<b>Цель проекта</b> — автоматизация функции учета посещаемости учебных занятий в формате мобильного приложения.

<b>Задачи разработки приложения:</b>

1) упрощение процесса учета посещаемости учебных занятий
   преподавателями и старостами групп
2) предоставление студентам возможности наблюдения своей
   посещаемости

<span style="color: #ff9243">**API**</span><br>

1. **Авторизация/Регистрация**
    - [http://127.0.0.1:8000/api/login/](http://127.0.0.1:8000/api/login/)
      отправить запрос методом <span style="color: #6FD8FA">**POST**</span>
      ```json 
        {
          "login": "", 
          "password": "", 
          "is_staff": "True"
        }
      ```
    - Если авторизация/регистрация прошла успешно сервер вернет код <span style="color:#FAE36F">**201**</span> и
      <span style="color:#C39EFF">*json*</span> в котором содержится <span style="color:#FAE36F">**access_token**</span>
      и <span style="color:#FAE36F">**refresh_token**</span> пользователя
      ```json
        {
           "access_token": "",
           "refresh_token": ""
        }     
      ```
2. **Обновление токена**
    - [http://127.0.0.1:8000/api/refresh/](http://127.0.0.1:8000/api/refresh/)
      отправить запрос методом <span style="color: #6FD8FA">**POST**</span> с указанием <span style="color:#FAE36F">*
      *refresh_token**</span>
      ```json
        {
           "refresh_token": ""
          }     
      ```
    - Если обновление токена прошло успешно сервер вернет код <span style="color:#FAE36F">**200**</span> и
      <span style="color:#C39EFF">*json*</span> в котором содержится <span style="color:#FAE36F">**access_token**</span>
      и <span style="color:#FAE36F">**refresh_token**</span> пользователя
      ```json
        {
           "access_token": "",
           "refresh_token": ""
        }     
      ```
