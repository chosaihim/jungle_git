#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"



int main()
{

	NODE* root = createNode();
	root->N = 0;
	root->isLeaf = true;

	insert(&root, 100);
	deleteKey(&root, 100);
	insert(&root, 99);
	insert(&root, 120);
	insert(&root, 110);
	insert(&root, 10);
	insert(&root, 20);
	insert(&root, 50);
	insert(&root, 105);

	traverse(root, 0);

	return 0;
}





