#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "header.h"


// ?��??��? ????��? ????�ƨ���?
#define DEGREE 8

int MIN_DEGREE = (int)((DEGREE + 1) / 2);
int MAX_DEGREE = DEGREE - 1;

Node* createNode()
{
	Node* newNode = (Node*)malloc(sizeof(Node));
	//int MIN_DEGREE = ceil(DEGREE/2);
	// ????��? ��?��? ??��? ��??????? ???��?�� ?? ��????? ?��???? ???��?��????
	// ex_ int ???��?? ��??? ?��???����? int *?? ??????��?.
	Node** children = (Node**)malloc((DEGREE + 1) * sizeof(Node*));
	int* key = (int*)malloc(DEGREE * sizeof(int));

	newNode->C = children;
	newNode->Key = key;


	return newNode;
}

// return 0 or 1
int searchNode(Node* root, int k)
{
	int idx = (root->N) - 1;
	while (idx >= 0 && root->Key[idx] > k)
	{
		idx--;
	}
	// ��? ��?��?? : NO !!
	// ????��? ??��? ?��?? ��?��??? ��??? ????���� ???��
	if (idx < 0 || root->Key[idx] != k)
		idx++;

	// ?��???����??
	if ((idx < root->N) && (k == root->Key[idx]))
	{
		return 1;
	}
	// ?��?��??��?, ��????��
	else if (root->isLeaf)
	{
		// ��??��?����? NULL
		return 0;
	}
	// ��??��??��?, ��??? ??��??��
	else
	{
		return searchNode(root->C[idx], k);
	}
}


void insertTree(Node** root, int k)
{
	Node* tmp = *root;
	if (((*root)->N == MAX_DEGREE))
	{
		// ��???��? ?? ��??? ????
		Node* to_be_root = createNode();
		*root = to_be_root;
		to_be_root->isLeaf = false;
		to_be_root->N = 0;
		to_be_root->C[0] = tmp;
		splitChild(to_be_root, 0);
		insertNonfull(to_be_root, k);
	}
	else
	{
		insertNonfull(*root, k);
	}
}

void splitChild(Node* parent, int idx)
{

	Node* right = createNode();
	Node* left = parent->C[idx];
	right->isLeaf = left->isLeaf;
	right->N = MIN_DEGREE - 1;
	for (int i = 0; i < MIN_DEGREE - 1; i++)
	{
		// ?????? ?��?��????
		right->Key[i] = left->Key[i + MIN_DEGREE];
	}
	if (!left->isLeaf)
	{
		for (int i = 0; i < MIN_DEGREE; i++)
		{
			right->C[i] = left->C[i + MIN_DEGREE];
		}
	}
	left->N = MIN_DEGREE - 1;
	// ??��? ????��? ��??? ??��? ��?��?
	for (int i = parent->N; i >= idx + 1; i--)
	{
		parent->C[i + 1] = parent->C[i];
	}
	parent->C[idx + 1] = right;
	// ?�� ????��? ��??? ??��? ��?��?
	for (int i = parent->N - 1; i >= idx; i--)
	{
		parent->Key[i + 1] = parent->Key[i];
	}
	// ??����?? ?�� ?��??
	parent->Key[idx] = left->Key[MIN_DEGREE - 1];
	parent->N++;
}

void insertNonfull(Node* root, int k)
{
	int num = (root->N) - 1;
	if (root->isLeaf)
	{
		while ((num >= 0) && (k < root->Key[num]))
		{
			root->Key[num + 1] = root->Key[num];
			num--;
		}
		root->Key[num + 1] = k;
		root->N = (root->N) + 1;
	}
	else
	{
		while ((num >= 0) && (k < root->Key[num]))
		{
			num--;
		}
		// ��?��? ????��? ��?�ƨ� ?��?? ?��????
		num++;

		// ��?��? ????��? ??��????? ��??? ???����?
		if (root->C[num]->N == MAX_DEGREE)
		{
			splitChild(root, num);
			// split ?? root?? ��??? ?����???��??? ��?��? ???����? ????��? ?? ��?��? ????
			if (k > root->Key[num])
				num++;
		}
		insertNonfull(root->C[num], k);
	}
}

void deleteTree(Node** root_address, Node* root, int k)
{
	int isIn = searchNode(root, k);
	if (isIn) {
		int idx = (root->N) - 1;

		// ��????? ?��?��???? ?��?? ?��??��?, ��??����? ??����?? ��??����? ?�� ????
		while (idx >= 0 && root->Key[idx] > k)
		{
			idx--;
		}

		// ��? ��?��?? : NO !!
		// ????��? ??��? ?��?? ��?��??? ��??? ????���� ???��
		if (idx < 0 || root->Key[idx] != k)
			idx++;

		// ��? ��????? (= ��?��? ????��??? ?????? idx)
		const int goal_idx = idx;

		// ��? ��?��??
		if (root->Key[goal_idx] == k)
		{
			//��? ��????�� ?
			//YES
			if (root->isLeaf)
			{
				// ??????
				for (int i = goal_idx; i < (root->N) - 1; i++)
				{
					root->Key[i] = root->Key[i + 1];
				}
				// ��?��? ��??? ???? ????????
				root->N--;
			}
			//NO -> ��? ????��??��??
			else
			{
				Node* Left = root->C[goal_idx];
				Node* Right = root->C[goal_idx + 1];
				int num_left = Left->N;
				int num_right = Right->N;

				// ??????
				if (Left->N >= MIN_DEGREE)
				{
					int tmp = Left->Key[num_left - 1];
					deleteTree(&Left, Left, tmp);
					root->Key[goal_idx] = tmp;

				}

				// ??????
				else if (Right->N >= MIN_DEGREE)
				{
					//int num_right = Right->N;
					int tmp = Right->Key[0];
					deleteTree(&Right, Right, tmp);
					root->Key[goal_idx] = tmp;
				}

				// ??��? ??????
				else
				{


					// ???? ??��??? ��??? ??��??? ??��? ??????
					Left->Key[num_left] = k;
					for (int i = 0; i < num_right; i++)
					{
						Left->Key[(num_left + 1) + i] = Right->Key[i];
					}

					// ????????
					if (!(Left->isLeaf))
					{
						for (int i = 0; i <= num_right; i++)
						{
							Left->C[(num_left + 1) + i] = Right->C[i];
						}
					}

					Left->N = MAX_DEGREE;
					free(Right);

					// ??���� ?�� & ??��? ??????
					for (int i = goal_idx; i < (root->N) - 1; i++)
					{
						root->Key[i] = root->Key[i + 1];
						root->C[i + 1] = root->C[i + 2];
					}
					root->N--;

					if (root->N == 0)
					{
						*root_address = Left;
					}

					// ?????? + ?????? ??��? //

					// ???? ????

					deleteTree(&Left, Left, k);

				}

			}
		}
		// ��? ???? ��????? ????.
		else
		{

			Node* Target = root->C[goal_idx];
			int num_Target = Target->N;

			// ��?��?��? �ơ�?? MIN_DEGREE?�� (?????��?? ) -> ???��??��? ����??��??��
			if (Target->N < MIN_DEGREE)
			{
				int right_idx = goal_idx + 1;
				int left_idx = goal_idx - 1;
				// merge (merge_target , ��?)
				// merge (��? , merge_target)

				// ??��??????? ��??? ?����? (RIGHT ???��?? ???�� ??��? ��??? ?? block ?????�� < bc : idx error)
				if (goal_idx != root->N && root->C[goal_idx + 1]->N >= MIN_DEGREE)
				{
					// ??��?????
					Node* Target_Right = root->C[goal_idx + 1];

					// ��? ��?��???
					Target->Key[num_Target] = root->Key[goal_idx];

					//?��???? ??��?????
					Target->C[num_Target + 1] = Target_Right->C[0];
					Target->N++;

					//��??? ?�� ��? ??��???
					root->Key[goal_idx] = Target_Right->Key[0];

					//???? ?�� ??????,
					//???? ?��???? ??????

					for (int i = 0; i < (Target_Right->N) - 1; i++)
					{
						Target_Right->Key[i] = Target_Right->Key[i + 1];

					}
					for (int i = 0; i < (Target_Right->N); i++)
					{
						Target_Right->C[i] = Target_Right->C[i + 1];
					}
					Target_Right->N--;
				}
				// ???? ???? ??��?
				else if (goal_idx != 0 && root->C[goal_idx - 1]->N >= MIN_DEGREE)
				{
					// ??��?????

					Node* Target_Left = root->C[goal_idx - 1];
					int num_Left = Target_Left->N;

					// ?����? ????��???
					for (int i = Target->N; i > 0; i--)
					{
						Target->Key[i] = Target->Key[i - 1];
					}
					// ��? ��?��???
					Target->Key[0] = root->Key[goal_idx - 1];

					// ?��???? ????��???
					for (int i = Target->N + 1; i > 0; i--)
					{
						Target->C[i] = Target->C[i - 1];
					}
					Target->C[0] = Target_Left->C[num_Left];
					Target->N++;

					root->Key[goal_idx - 1] = Target_Left->Key[num_Left - 1];

					Target_Left->N--;


				}

				// ��? ????��? ��? ????
				else
				{
					//��?��? ��??? ?�� ?????��, ��?��? ??????��?���� ?????��??
					if (goal_idx == root->N)
					{
						// merge_left
						Node* Target_Left = root->C[goal_idx - 1];
						int num_Left = Target_Left->N;
						//mergeNode(Left, Target);
						// Target = Left
						Target_Left->Key[num_Left] = root->Key[goal_idx - 1];

						// ?????? ??��??? ?��?��???? ??????��??��
						for (int i = 0; i < Target->N; i++)
						{
							Target_Left->Key[(num_Left + 1) + i] = Target->Key[i];
						}
						for (int i = 0; i <= Target->N; i++)
						{
							Target_Left->C[(num_Left + 1) + i] = Target->C[i];
						}
						Target_Left->N = MAX_DEGREE;
						root->N--;
						// root ��? ??��?��?? 
						if (root->N == 0)
						{
							*root_address = Target_Left;
						}

						free(Target);

						Target = Target_Left;
					}
					else
					{
						// merge_right
						// ??��??? ?????? ????
						Node* Target_Right = root->C[right_idx];
						// ??���� ��? ?��?? ��???


						//mergeNode(Target, Right);
						Target->Key[num_Target] = root->Key[goal_idx];

						for (int i = 0; i < Target_Right->N; i++)
						{
							// ??????��??? ??��??? ??��? ?�� ��???
							Target->Key[(num_Target + 1) + i] = Target_Right->Key[i];

						}
						if (!(Target->isLeaf))
						{
							for (int i = 0; i <= Target_Right->N; i++)
							{
								// ???? ??��??? Child?? ??��??? ??��??? Child ��???
								Target->C[(num_Target + 1) + i] = Target_Right->C[i];

							}
						}
						Target->N = MAX_DEGREE;

						for (int i = goal_idx; i < (root->N) - 1; i++)
						{
							root->Key[i] = root->Key[i + 1];
							root->C[i + 1] = root->C[i + 2];
						}
						root->N--;
						if (root->N == 0)
						{
							*root_address = Target;
						}

						// ??��? ��?��??? ???��.
						// ??????��??? ?��?��??��? ??��???, ??????��??? ????��? ?????�� free��? ��?????��?.
						free(Target_Right);




					}
				}
			}


			deleteTree(&Target, Target, k);


			// ???? ?����? (LEFT ???��?? ???�� ??��? ��??? ?? block ?????��)

		}
	}
	else
	{
		//printf("The key is not in the Tree");
	}
}
// ��??? ??��? ??��?????(?)
//void printAll(Node* root, int depth)
//{
//	
//	// depth����?�� ?��??
//	for (int i = 0; i < depth; i++)
//	{
//		printf("\t");
//	}
//	
//	for (int i = 0; i <= root -> N; i++)
//	{
//		if (root->C[i]->N != 0)
//		{
//			printf("%d\n", root->Key[i]);
//			printAll(root->C[i]);
//			printf("\n");
//		}
//	}
//	
//}
void printAll(Node* root, int depth)
{
	printf("\n");
	Node* node = root;
	if (node->isLeaf) {
		for (int i = 0; i < depth; i++) {
			printf("\t\t\t||");
		}
		for (int vIdx = 0; vIdx < node->N; vIdx++) {
			printf("%6d", node->Key[vIdx]);
		}
		return;
	}
	if (!node->isLeaf) {
		for (int i = 0; i < depth; i++) {
			printf("\t\t\t||");
		}
		for (int vIdx = 0; vIdx < node->N; vIdx++) {
			printf("%6d", node->Key[vIdx]);
		}
		for (int vIdx = 0; vIdx < node->N + 1; vIdx++) {
			printAll(node->C[vIdx], depth + 1);
		}
	}
}