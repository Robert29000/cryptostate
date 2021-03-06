# Курсовой проект 

## Создание ERC20-токена с KYC процедурой. Применение его в государственной системе.

![Alt text](/pics/intro.jpg)

### Описание проекта

Цель проекта является разработать государственную систему для борьбы с коррупцией на базе блокчейна. Основываться данная система будет на ERC20-токене, с которым будут проходить все операции в новой инфраструктуре. Особенностью токена является возможность проводить с ним операции только адресам, прошедшим проверку. Также для избежания централизации сам контракт будет иметь несколько владельцев. В рамках государства это могут быть банки или финансовые структуры, которые смогут подкрепить токен фиатными деньгами. Соответственно при переводе экономической системы на новую на базе блокчейна, компании, работающие с государством, должны будут использовать для расчетов этот токен. Это позволит сделать деятельность компаний более прозрачной, избежать недобросовестных или мошеннических схем (т.к. они должны пройти проверку нескольких банков или структур). Сам блокчейн можно сделать на базе Ethereum с использованием PoA-консенсуса, где валидаторы будут принадлежать владельцам смарт-контракта-токена

### Описание CryptoState токена

![Alt text](/pics/token.jpg)

Данный токен основывается на стандарте ERC20 и реализует его интерфейс с некоторыми дополнениями. Стандартные операции ```transfer```, ```transferFrom```, ```approve``` проходят дополнительные проверки адресов. Благодаря использованию библиотеки **SafeMath** в некоторых методых опущены проверки операций, так как они уже реализованы в билиотеке. По задумке токен принадлежит нескольким владельцам, которые вместе со своими адресами предоставляют количество монет, которые могут обеспечить. Функции связанные с изменением общего количества монет, изменением владельцев могут быть осуществлены только **Owner-ами**. Также на них лежит задача проверки адресов, которые хотят использовать этот токен. Все операции разрешены только адресам, прошедшим проверку. Для этого каждый адрес в параметрах и **msg.sender** проверяются модификаторами. Говоря о децентрализации, был использован паттерн **MultiOwnable**, который позволяет указать владельцев и необходимое количество подтверждений для валидации операции. Благодаря структуре **Operation**, контракт-наследник может реализовать любую функцию, требущую участия нескольких сторон.

### Описание смарт-контрактов, использующих данный токен. Описание StatePurchase

Использование данного токена, требует более сложных подготовительных операций, нежели при работе с эфиром. Как пример контракта, работающего на базе **CryptoState**, я создал простой смарт-контракт для совершения покупок. Для того, чтобы смарт-контракт смог работать с балансами покупателя и продавца, он должен пройти такую же проверку и получить **approve** у клиентов. Для предотвращения Reentrency-атаки используется переменная **State** и модификаторы. Для удобства работы я создал отдельный контракт по паттерну *Фабрика*, где можно создавать для каждой продажи отдельный **StatePurchase**. После получения адреса, созданного контракта, его необходимо заверить, как и обычный адрес пользователя. 

### Построение PoA блокчейна

![Alt text](/pics/poa.jpg)

В процессе выбора алгоритма консенсуса самым оптимальным оказалася PoA. Он не требует больших вычислительных мощностей и полностью финализирован. Для того, чтобы валидаторы не концентрировались у одного владельца и во избежании централизации, каждый финансовый институт, который обеспечивает токен, будет держать своего валидатора. В данном разделе приведу пример настройки простой приватной PoA сети. 

1) Для начала создадим в корне проекта папки с данными нод три аккаунта. Сделаем это с помощью следующих команд:

```sh
$ geth --datadir node1/ account new 
$ geth --datadir node2/ account new 
$ geth --datadir node3/ account new
```
2) В файле **genesis.json** нужно прописать адреса, созданных аккаунтов в разделе **alloc**. После этого можно инициализировать ноды:

```sh
$ geth --datadir node1/ init genesis.json
$ geth --datadir node2/ init genesis.json
$ geth --datadir node3/ init genesis.json
```

3) Для того, чтобы объединить все ноды в одну частную сеть, используется *boot-нода*. Для ее инициализации пропишем следующие команды:

```sh
bootnode -genkey boot.key
bootnode -nodekey boot.key -verbosity 9 -addr :<bootport>
```
4) После команд в консоли выведется информация о адресе *boot-ноды* в формате <enode://<Identifier>@<IP-address>:0?discport= <bootport> >

5) Теперь можем запустить ноды. В параметрах ```--port``` и ```--rpcport``` указываем уникальные порты для каждой ноды. Для старта нужно разблокировать аккаунт валидатора. Это можно сделать с помощью следующих параметров:

```sh
$ geth --datadir node2/ --syncmode 'full' --port <port number 1> -rpc --bootnodes "адресс boot-ноды, выведенный в пункте 4" --rpcport <port number 2> --mine --unlock <аккаунт валидатора> --allow-insecure-unlock
```
6) На этом этапе уже можно деплоить контракты в сеть
### To-Do
- [ ] Покрыть тестами все функции контрактов
- [ ] В **CryptoState** и **Multiownable** просмотреть логику отмены подтверждения операции, лишение адреса KYC-проверки
- [ ] Разобраться в юридических тонкостях процедуры прохождения KYC-процедуры юридическими лицами
- [ ] Расширять набот контрактов на базе данного токена. Одним из главных будет смарт-контракт для аукционов. Он позволит проводить гос. тендеры и закупки


