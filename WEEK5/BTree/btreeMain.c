#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "header.h"


int main()
{
	Node* root = createNode();
	root->N = 0;
	root->isLeaf = true;

	int val = 0;
	int flag = 0;
	for (int i = 0; i < 1000; i++)
	{
		val = rand();
		val %= 1000;
		flag = searchNode(root, val);
		if (flag==1)
			continue;
		insertTree(&root,val );
		continue;
		//printf("%d %d\n", i,val);
	}

	for (int i = 0; i < 500; i++)
	{
		val = rand();
		val %= 1000;
		flag = searchNode(root, val);
		if (flag == 0)
			continue;
		
		deleteTree(&root,root, val);
		continue;
		//printf("%d %d\n", i, val);

	}
	printAll(root, 0);
	//printAll(root, 0);



	return 0;
}