#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"

#define TEST { 10,1,3,63,82,6,31,8,2,16,11,77,96,14,92,21,47,23,24,78,26,97,15,4,30,69,37,38,76,90,17,87,53,44,45,46,9,41,54,43,22,84,58,39,65,28,42,59,99,70,71,72,29,74,73,68,13,60,79,80,81,85,83,64,94,86,66,88,93,40,91,62,25,20,36,95,19,52,55,100 }





int main()
{

	int arr[80] = TEST;
	NODE* root = createNode();
	root->N = 0;
	root->isLeaf = true;

	// TEST 1 CASE
	insert(&root, 4, 4 * 1000);
	insert(&root, 1, 1 * 1000);
	insert(&root, 3, 3 * 1000);
	insert(&root, 2, 2 * 1000);

	deleteKey(&root, 4);
	deleteKey(&root, 2);
	deleteKey(&root, 3);

	printf("---- TEST1 ----\n");
	print_for_exam(root);

	// TEST 2 CASE
	for (int i = 2; i <= 100; i++) {
		insert(&root, i, i * 1000);
	}

	for (int i = 50; i <= 70; i++) {
		deleteKey(&root, i);
	}

	//for (int i = 1; i <= 20; i++) {
	//	insert(&root, i, i * 1000);
	//}
	//traverse(root, 0);
	//deleteKey(&root, 5);
	//traverse(root, 0);


	//for (int i = 5; i <= 7; i++) {
	//	//printf("\n--------------del: %d--------------\n", i);
	//	deletekey(&root, i);
	//}


	printf("\n\n\n\n\n\n");
	printf("---- TEST2 ----\n");
	print_for_exam(root);

	// TEST3 CASE
	for (int i = 50; i <= 70; i++) {
		insert(&root, i, i * 1000);
	}

	for (int i = 0; i < 80; i++) {
		deleteKey(&root, arr[i]);
	}

	printf("\n\n\n\n\n\n");
	printf("---- TEST3 ----");
	print_for_exam(root);

	printf("프로그램이 정상적으로 종료 되었음.");


	return 0;
}

