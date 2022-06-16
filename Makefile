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

clean:
	rm *.html *.csv

.PHONY: format check_formatting clean