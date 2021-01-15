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

	//printf("차수를 입력하세요 : ");
	//scanf("%d", DEGREE);
	//MAX_DEGREE = (int)((DEGREE + 1) / 2);
	//MIN_DEGREE = DEGREE - 1;


	while (1)
	{
		int input = 0;
		int val = 0;
		int flag = 0;
		int issearch = 0;
		printf("\n1.조회\t2/삽입\t3.삭제\t4.출력\t5.종료 :");
		scanf("%d", &input);

		switch (input) {
		case 1:
			printf("값을 입력하세요 : ");
			scanf("%d", &val);
			issearch = searchNode(root, val);
			if (issearch)
				printf("값이 존재합니다 !! ㅎㅎ");
			else
				printf("값이 존재하지 않습니다. ㅠㅠ");
			break;
		case 2:
			printf("값을 입력하세요 : ");

			scanf("%d", &val);

			if (!searchNode(root, val))
				insertTree(&root, val);

			break;

		case 3:
			printf("값을 입력하세요 : ");
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
			printf("인식할 수 없는 값입니다.");
			break;
		}
		if (flag)
			break;
	}

	/* 랜덤 값 넣어서 디버깅 */

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
