# smart-contract-test
smart contract from solidity by example deploy and test (web3.py, ganache, truffle)

![image](https://user-images.githubusercontent.com/61321903/170150708-a8ca5d15-74fa-4be0-9aa9-2bb8b764179b.png)

Контракт Ballot (файл «voting.sol»), взятый из документации Solidity, реализует логику электронного голосования. В нём объявляется структура Voter, отвечающая за голосующие узлы, и Proposal, представляющая кандидатов голосования. При развертывании контракта назначается председатель (chairman), который может предоставлять узлам сети возможность голосовать (giveRightToVote()). У каждого, кто получил это право, есть возможность либо проголосовать самому (vote()), либо выбрать делегата и передать ему свой голос (delegate()). Расчёт голосов производится за счёт накопления веса (weight) у выбранных делегатов и суммирования в voteCount для каждого из кандидатов значений веса проголосовавших за них узлов. На основе полученных значений функция winningProposal() определяет индекс победителя в массиве кандидатов, а winnerName() по данному индексу возвращает адрес узла-победителя.
Дальнейшая работа с кодом контракта происходит в файле «deploy.py», где он компилируется с помощью py-solc-x. В результате компиляции мы получаем байт-код контракта и abi – json описание всех функций и переменных контракта. Для взаимодействия контракта с локальной сетью, развёрнутой с помощью фреймворка Ganache, необходимо установить библиотеку web3.py. После получения контракта из его байт-кода и abi необходимо собрать транзакцию (buildTransaction()), подписать её с помощью приватного ключа и отправить. Взаимодействие с развёрнутым в локальной сети контрактом представлено в файле «interaction.py». Аналогично с помощью Truffle возможно тестирование контракта на одной из тестовых сетей Ethereum, например, на Rinkeby.
