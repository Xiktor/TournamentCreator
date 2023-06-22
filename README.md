Readme w wersji pdf: [README.pdf](https://github.com/Xiktor/TournamentCreator/files/11833655/README.pdf)


# Cel projektu
Wykorzystując jeden z dostępnych framework'ów opartych na ORM (i / lub architekturze REST) napisz aplikację pozwalającą rozgrywać turnieje w systemie pucharowym.
Wymagania funkcjonalne:

•	Użytkownik rejestruje się w aplikacji podając dane, takie jak adres email, nazwa, data urodzenia, hasło. 

•	Użytkownik loguje/wyloguje się z aplikacji.

•	Użytkownik tworzy nowy turniej podając jego nazwę, datę i godzinę rozpoczęcia oraz maksymalną ilość graczy.

•	Użytkownik usuwa turniej z systemu.

•	Użytkownik dodaje nowych graczy i przyporządkowuje je do określonego turnieju.

•	Użytkownik wpisuje wyniki pojedynków w kolejnych fazach turnieju.

•	Użytkownik przegląda historyczne turnieje z określonego przedziału czasu

Wymagania pozafunkcjonalne:

•	Parowanie graczy w pierwszej fazie turnieju jest losowe.

•	W aplikacji istnieją min. 3 grupy użytkowników różniące się uprawnieniami: Administratorzy, Użytkownicy zwykli, Użytkownicy anonimowi.

•	Użytkownik anonimowy posiada uprawnienia tylko do przeglądania rozpoczętych turniejów.

•	Użytkownik zwykły zarządza turniejami przez siebie utworzonymi, przy czym nie ma możliwości usuwania i edycji turnieju gdy ten już się rozpoczął.

•	Administrator może wszystko. W tym dodać nowe konto administratora

# Stack technologiczny
Aplikacja jest napisana w języku Python z użyciem frameworka Django, w oparciu o architekturę MVT (Model-View-Template). Zastosowano plikową bazę danych SQLite.
Django dzięki wbudowanym modułom zapewnia:

•	gotowy model użytkownika oraz widoki uwierzytelniania(django.contrib.admin)

•	uwierzytelnianie i autoryzacja użytkownika(django.contrib.auth),

•	obsługiwanie sesji użytkownika(django.contrib.session), 

•	ochronę przed atakami CSRF z użyciem tokenów CSRF (django.middleware.csrf.CsrfViewMiddleware)

•	walidację siły hasła(AUTH_PASSWORD_VALIDATORS)

# Uruchomienie projektu
Aby uruchomić projekt proszę wprowadzić ścieżkę do interpretera pythona.
Zainstalować pakiety zawarte w requirements.txt, tj.

**python -m pip install Django**

**pip install numpy**

Następnie można uruchomić projekt

**python manage.py runserver**

W bazie są już dwa konta z przykładowymi danymi, konto administratora:

**login:	superUser**

**haslo:	user12345**

oraz konto zwykłego użytkownika

**login: 	user**

**haslo: 	user12345**

Projekt został utworzony w IDE PyCharm.

# Zrzuty ekranu

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/c72fd0b1-8a7f-494e-a334-6dc2dc24305a)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/acaf8751-5170-49ab-bc13-8cb21435b844)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/a3abd6f0-7e16-494f-9d9a-1037f7278835)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/cb111d7b-ee60-4877-8e40-0c6dd7d942ae)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/e9ad19f6-0826-4dfb-ae23-9196a0fb8ca2)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/51f5a29d-b771-4288-8547-f2653f17e8f3)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/ff7b7c8e-6914-424f-8332-d13659709b72)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/f8ec1cd3-d658-463f-b6ec-38285144b03f)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/62ecb166-6fd5-4d9d-84ed-5f9280d73ef4)

![image](https://github.com/Xiktor/TournamentCreator/assets/62425432/9d576f37-40a7-4d12-a219-3d930e2563af)


