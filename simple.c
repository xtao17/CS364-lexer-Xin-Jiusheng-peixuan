int sum_3_or_5 (int n) {
	int sum;
	int i;
	sum = 0;
	i = 0;
		while (i < n) {
			if(((i % 3 + 2 - 1) == 0) || ((i % 5) == 0))
				sum = (sum + i);
 				i = (i + 1);

		}
	return sum;
}

int main (int u) {
	int i;
	i = 1 + 2 - 3;
}
