INSTRUKCJA KORZYSTANIA Z PLIKU TRANSFORMACJE.PY

1. DO CZEGO SŁUŻY PROGRAM?
	Program ma za zadanie transformować współrzędne podane w pliku tekstowym dla podanego modelu elipsoidy (do wyboru 3: "WGS84", "GRS80" i
	elipsoida Krasowskiego. Dla transformacji ze wsp. geocentrycznych na wsp. geodezyjne przewidziany jest też wybór jednostki: stopnie 
	dziesiętne albo stopnie/minuty/sekundy. Program obsługuje transformacje: XYZ - PLH, PLH - XYZ, XYZ - NEUp, PL - XY PL-2000 i
	PL - XY PL_1992.

2. JAKIE SĄ WYMAGANIA, BY PROGRAM DZIAŁAŁ NA KOMPUTERZE?
	Aby program działał prawidłowo użytkownić musi posiadać na swoim komputerze zainstalowaną bibliotekę Numpy oraz skonfigurowane
	środowisko Pythona. Dodatkowo zainstalowaną wersją Pythona powinna być wersja 3.11, aczkolwiek skrypt powinien zadziałać też 
	dla wersji 3.12.

3. DLA JAKIEGO SYSTEMU OPERACYJNEGO ZOSTAŁ NAPISANY PROGRAM?
	Program został napisany i testowany dla systemu Windows. Według naszej wiedzy działa on tylko na nim, nie oznacza to jednak, że
	program ten nie zadziałałby na urządzeniu o innym systemie operacyjnym.
	
4. JAK UŻYWAĆ PROGRAMU?
	Aby użyć programu trzeba spełnić ww. wymagania. Po spełnieniu ich należy uruchomić wiersz poleceń w folderze instalacyjnym programu
	(w moim przypadku ścieżka: "C:\Users\Julka\Desktop\Studia\Informatyka geodezyjna II\PROJEKT INF\projekt_informatyka").
	Po uruchomieniu programu należy wpisać komendę w następującego kolejności:
	python transformacje.py [transformacja] [jednostka] [model_elipsoidy] [plik_ze_wspolrzednymi]
	  
	Niżej podane są wartości zmiennych (takie nazwy należy podawać, by program zadziałał):
	  
	transformacja: xyz2plh, plh2xyz, xyz2neu, pl2xygk2000, pl2xygk1992
	jednostka: dec_degree, dms, bez_jednostki (jednostkę podaje się jedynie, gdy wybraliśmy transformację xyz2plh)
	model_elipsoidy: wgs84, grs80, krasowski
	plik_ze_wspolrzednymi: jakakolwiek nazwa

5. PRZYKŁADOWE WYWOŁANIA PROGRAMU
	python transformacje.py xyz2plh dec_degree wgs84 wsp_xyz.txt
	python transformacje.py plh2xyz bez_jednostki krasowski wsp_plh.txt
	python transformacje.py xyz2neu bez_jednostki grs80 wsp_xyz.txt
	python transformacje.py pl2xygk2000 bez_jednostki wgs84 wsp_plh.txt
	python transformacje.py pl2xygk1992 bez_jednostki grs80 wsp_plh.txt
	
	Gdy program zostanie wywołany, jego prawidłowe wykonanie jest potwierdzone wiadomością: 
	"Program został wykonany poprawnie :)".
	
6. PRZYKŁADOWY PLIK ZE WSPÓŁRZĘDNYMI
	Program został napisany dla przykładowych plików ze współrzędnymi (są podane w folderze z kodem).
	Program pozbywa się pierwszych czterech linijek i następnie dzieli poniższe linie na części i przypisuje odpowiedniej zmiennie
	odpowiednią część linii. Linie ze współrzędnymi mają się prezentować następująco: X,Y,Z (bez spacji między).

7. BŁĘDY I NIETYPOWE ZACHOWANIA PROGRAMU
	Podczas pisania programu nie napotkaliśmy żadnych problemów.