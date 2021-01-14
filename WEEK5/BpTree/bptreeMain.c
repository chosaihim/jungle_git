#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"


int main()
{
	Node* root = createNode();
	root->N = 0;
	root->isLeaf = true;

	//printf("������ �Է��ϼ��� : ");
	//scanf("%d", DEGREE);
	//MAX_DEGREE = (int)((DEGREE + 1) / 2);
	//MIN_DEGREE = DEGREE - 1;


	while (1)
	{
		int input=0;
		int val = 0;
		int flag = 0;
		int issearch = 0;
		printf("\n1.��ȸ\t2/����\t3.����\t4.���\t5.���� :");
		scanf("%d", &input);

		switch (input) {
		case 1:
			printf("���� �Է��ϼ��� : ");
			scanf("%d", &val);
			issearch = searchNode(root, val);
			if (issearch)
				printf("���� �����մϴ� !! ����");
			else
				printf("���� �������� �ʽ��ϴ�. �Ф�");
			break;
		case 2:
			printf("���� �Է��ϼ��� : ");

			scanf("%d", &val);

			if (!searchNode(root, val))
				insertTree(&root, val);
			
			break;
				
		case 3:
			printf("���� �Է��ϼ��� : ");
			scanf("%d", &val);

			if (searchNode(root, val))
				deleteTree(&root, val);
			break;
		case 4:
			printAll(root, 0);
			break;
		case 5:
			flag = 1;
			break;
		default:
			printf("�ν��� �� ���� ���Դϴ�.");
			break;
		}
		if (flag)
			break;
	}

	/* ���� �� �־ ����� */

	//int val = 0;
	//int flag = 0;
	//for (int i = 0; i < 10000; i++)
	//{
	//	val = rand();
	///*	val %= 100;*/
	//	flag = searchNode(root, val);
	//	if (flag==1)
	//		continue;
	//	insertTree(&root, val);
	//	continue;
	//	//printf("%d %d\n", i,val);
	//}

	//for (int i = 0; i < 10000; i++)
	//{
	//	val = rand();
	//	//val %= 100;
	//	flag = searchNode(root, val);
	//	if (flag == 0)
	//		continue;
	//	
	//	deleteTree(&root, val);
	//	continue;
	//	//printf("%d %d\n", i, val);

	//}

	//printAll(root, 0);








	return 0;
}
