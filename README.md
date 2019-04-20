# rulemma - лемматизатор для русскоязычных текстов для R&amp;D в NLP

Этот лемматизатор написан полностью на Питоне, что позволяет при необходимости
модифицировать его выдачу под конкретную задачу - в этом причина упоминания "R&D"
в описании.

Подготовленная модель лемматизации включена в библиотеку, поэтому
лемматизатор полностью готов к использованию после установки.

Для установки достаточно выполнить в консоли:

```
pip3 install git+https://github.com/Koziev/rulemma
```

## Пример использования

На вход лемматизатор принимает результаты частеречного разбора, который
выполняется отдельной библиотекой [rupostagger](https://github.com/Koziev/rupostagger).
В свою очередь частеречная разметка выполняется по результатам токенизации, которую
можно выполнить с помощью [rutokenizer](https://github.com/Koziev/rutokenizer).

Следующий код выполнит лемматизацию предложения "Мяукая, голодные кошки ловят жирненьких мышек":

```
import rutokenizer
import rupostagger
import rulemma


lemmatizer = rulemma.Lemmatizer()
lemmatizer.load()

tokenizer = rutokenizer.Tokenizer()
tokenizer.load()

tagger = rupostagger.RuPosTagger()
tagger.load()

sent = u'Мяукая, голодные кошки ловят жирненьких хрюнделей'
tokens = tokenizer.tokenize(sent)
tags = tagger.tag(tokens)
lemmas = lemmatizer.lemmatize(tags)
for word, tags, lemma, *_ in lemmas:
	print(u'{:15}\t{:15}\t{}'.format(word, lemma, tags))
```

В результате будет выведено:

```
Мяукая         	мяукать        	VERB|VerbForm=Conv
,              	,              	PUNCT
голодные       	голодный       	ADJ|Case=Nom|Degree=Pos|Number=Plur
кошки          	кошка          	NOUN|Case=Nom|Number=Plur
ловят          	ловить         	VERB|Mood=Ind|Number=Plur|Person=3|Tense=Notpast|VerbForm=Fin
жирненьких     	жирненький     	ADJ|Case=Acc|Degree=Pos|Number=Plur
хрюнделей      	хрюндель       	NOUN|Case=Acc|Number=Plur
```

Обратите внимание на последний токен 'хрюнделей'. Лемматизатор содержит модель для обработки out-of-vocabulary слов,
и во многих случаях она нормально приводит слово к лемме, учитывая результаты частеречной разметки.
