test_image = dlmread("test_image.dat", "\t");
test_filter = dlmread("test_filter.dat", "\t");

result = conv2(test_image, test_filter, shape="same");
dlmwrite("coupled_filtering_test_result_octave.txt", result, "\t")