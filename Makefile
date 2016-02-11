all: mother_of_all_warehouses.out busy_day.out redundancy.out code.zip

%.out: data/%.in
	python titou.py $< > $@

code.zip: *.py
	zip $@ $^
