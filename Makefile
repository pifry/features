SRC = \
	main.py \
	dataset.py \
	presentation.py \
	video.py \
	features.py \
	features_plot.py \
	frame_features.py \
	global_features.py \


BLACK = black

format: $(SRC)
	$(BLACK) $^

check_formatting: $(SRC)
	$(BLACK) --check $^

test:
	python main.py -n 10 --ohtml output/result.html --ocsv output/result.csv --plots output/plots -j 5

clean:
	rm -r *.html *.csv output

.PHONY: format check_formatting clean test