#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>

#include "bptree.h"

#define DEGREE 4

int MIN_DEGREE = (int)((DEGREE + 1) / 2);
int MAX_DEGREE = DEGREE - 1;

Node* createNode()
{
	Node* newNode = (Node*)malloc(sizeof(Node));
	// ���԰������� �ʿ��Ͽ�, �ϳ��� �� �߰�
	Node** children = (Node**)malloc((DEGREE + 2) * sizeof(Node*));
	int* key = (int*)malloc((DEGREE + 1) * sizeof(int));

	newNode->C = children;
	newNode->Key = key;
	newNode->Next = NULL;

	return newNode;
}

int searchNode(Node* root, int k)
{
	int idx = (root->N);
	while (idx > 0 && root->Key[idx - 1] > k)
	{
		idx--;
	}
	
	// ������ �ƴϸ�
	if (!root->isLeaf)
		return searchNode(root->C[idx], k);

	else
	{
		idx--;
		// ã�Ҿ�
		if ((idx >= 0) && k == root->Key[idx])
			return 1;
		// ��ã�Ҿ�
		else
			return 0;
	}
	
}


void insertTree(Node** root, int k)
{


		Node* tmp = *root;
		if (((*root)->N == MAX_DEGREE))
		{
			// ��Ʈ�� �� ��� ����
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


void insertNonfull(Node* root, int k)
{
	int idx = (root->N) - 1;
	if (root->isLeaf)
	{
		while ((idx >= 0) && (k < root->Key[idx]))
		{
			root->Key[idx + 1] = root->Key[idx];
			idx--;
		}
		root->Key[idx + 1] = k;
		root->N = (root->N) + 1;
	}
	else
	{
		while ((idx >= 0) && (k < root->Key[idx]))
		{
			idx--;
		}
		// ���� �� ���� ���� ���־�
		idx++;

		// ���� �� �ڳ���� ���� á����
		if (root->C[idx]->N == MAX_DEGREE)
		{
			splitChild(root, idx);
			// split �� root�� ���� �߰��Ǵϱ� ���� ���� �� �� �ٽ� Ȯ��
			if (k > root->Key[idx])
				idx++;
		}
		insertNonfull(root->C[idx], k);
	}
}

void splitChild(Node* parent, int idx)
{

	Node* right = createNode();
	Node* left = parent->C[idx];
	right->isLeaf = left->isLeaf;
	//******************���� �����������************************
	//right->N = MIN_DEGREE - 1;

	// ���� ���� �����϶�, �θ����� �����ؼ� �÷��� (copy up)
	if (left->isLeaf)
	{

		right->Next = left->Next;
		left->Next = right;
		// �����ʿ� ������ �ް����� �־��ְ�
		for (int i = 0; i < MIN_DEGREE - 1; i++)
		{
			// ������ �׶�����
			right->Key[i] = left->Key[i + MIN_DEGREE];
			// ������, ���� ��� ��� C(�ڳ�)���� ���´�.
		}

		// ���� ��带 ����Ű�� ����
		right->N = MIN_DEGREE - 1;
		left->N = MIN_DEGREE;


		//(�θ�) �а�, �߰��ڸ� �ø���, �ڽ� �����Ű��
		// �ڽ� �ö� �༮ �ڸ� ����
		// idx N �̸�, parent-> N : N-1, idx : N �̶� for���� ���� ����!
		for (int i = parent->N; i >= idx; i--)
		{
			parent->C[i + 1] = parent->C[i];
		}
		// idx�� N�̾, ���� �߰��Ǵϱ�
		parent->C[idx + 1] = right;
		// Ű �ö� �༮ �ڸ� ����
		for (int i = parent->N - 1; i >= idx; i--)
		{
			parent->Key[i + 1] = parent->Key[i];
		}
		// �θ� Ű ����
		parent->Key[idx] = right->Key[0];
		parent->N++;

	}

	//������ �ƴϸ�, (B TREE �� ���� )
	else
	{
		// �����ʿ� ������ �ް����� �־��ְ�
		for (int i = 0; i < MIN_DEGREE - 1; i++)
		{
			// ������ �׶�����
			right->Key[i] = left->Key[i + MIN_DEGREE];
		}
		// ������, ���� ��� ��� C(�ڳ�)���� ���´�.
		for (int i = 0; i < MIN_DEGREE; i++)
		{
			right->C[i] = left->C[i + MIN_DEGREE];
		}

		left->N = MIN_DEGREE - 1;
		right->N = MIN_DEGREE - 1;

		// �ڽ� �ö� �༮ �ڸ� ����
		// idx N �̸�, parent-> N : N-1, idx : N �̶� for���� ���� ����!
		for (int i = parent->N; i >= idx; i--)
		{
			parent->C[i + 1] = parent->C[i];
		}
		// idx�� N�̾, ���� �߰��Ǵϱ�
		parent->C[idx + 1] = right;
		// Ű �ö� �༮ �ڸ� ����
		for (int i = parent->N - 1; i >= idx; i--)
		{
			parent->Key[i + 1] = parent->Key[i];
		}
		// �θ� Ű ����
		parent->Key[idx] = left->Key[MIN_DEGREE - 1];
		parent->N++;
	}

}

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

		printf("\t���� �ڽ��� : %p", node->Next);
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

void deleteTree(Node** root, int k)
{

	// �ȿ� ���� ���� ���� ����

	int idx = (*root)->N;

	// ������ �� ũ��, 0�� ���� ��
	// ���� ���� ũ�� N�� ������
	while (idx > 0 & (*root)->Key[idx - 1] > k)
	{
		idx--;
	}

	const int goal_idx = idx;

	// ���� �� ������?
	if ((*root)->isLeaf)
	{
		// ���� Key[goal_idx - 1]�̴�.
		for (int i = goal_idx - 1; i < ((*root)->N) - 1; i++)
		{
			(*root)->Key[i] = (*root)->Key[i + 1];
		}
		(*root)->N--;
	}
	// �����ƴϾ� ( == �� �� �� �� �־� !!)
	else
	{
		Node* Target = (*root)->C[goal_idx];
		if (Target->N < MIN_DEGREE)
		{
			// �ڽ��� �ȶ׶��ѵ�, ������
			if (Target->isLeaf)
			{
				// ������ ���� ��������, ������ ���� ������ ������.
				if (goal_idx == (*root)->N)
				{
					// �����´� -> ������ ��������, �θ� ������Ʈ �������
					Node* Sibling = (*root)->C[goal_idx - 1];
					if (Sibling->N >= MIN_DEGREE)
					{
						for (int i = Target->N; i > 0; i--)
						{
							Target->Key[i] = Target->Key[i - 1];
						}
						Target->Key[0] = Sibling->Key[(Sibling->N) - 1];
						Target->N++;
						Sibling->N--;

						(*root)->Key[goal_idx - 1] = Target->Key[0];
					}
					else
					{
						// ��ģ��.
						for (int i = 0; i < Target->N; i++)
						{
							Sibling->Key[(Sibling->N) + i] = Target->Key[i];

						}
						Sibling->N = Sibling->N + Target->N;
						free(Target);
						Target = Sibling;
						Target->Next = NULL;
						(*root)->N--;
						if ((*root)->N == 0)
						{
							//printf("\nroot�� �ٲ�ϴ� \n");
							*root = Target;
						}
					}

				}

				// �� �ܿ���, ������ ������ ������ ������.
				else
				{
					Node* Sibling = (*root)->C[goal_idx + 1];
					// ���� �׶��� ? -> �����ðž�
					if (Sibling->N >= MIN_DEGREE)
					{
						Target->Key[Target->N] = (*root)->Key[goal_idx];
						Target->N++;
						// �� Child �� Sibling ��������ش�.

						// ������ Ű �� ����.
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];

						}
						Sibling->N--;
						(*root)->Key[goal_idx] = Sibling->Key[0];
					}
					// ������ �ȶ׶��� -> ��ĥ�ž�
					else
					{
						for (int i = 0; i < Sibling->N; i++)
						{
							Target->Key[(Target->N) + i] = Sibling->Key[i];
						}
						Target->N = Target->N + Sibling->N;
						Target->Next = Sibling->Next;

						for (int i = goal_idx - 1; i < ((*root)->N) - 1; i++)
						{
							(*root)->Key[i] = (*root)->Key[i + 1];
							(*root)->C[i + 1] = (*root)->C[i + 2];
						}
						(*root)->N--;
						if ((*root)->N == 0)
						{
							//printf("\nroot�� �ٲ�ϴ� \n");
							*root = Target;
						}
						//free(Sibling);
					}
				}
			}
			// �ڽ��� �ȶ׶��ѵ�, ������ �ƴϾ�
			else
			{
				// ������ ���� ���ִ�.
				if (goal_idx == (*root)->N)
				{
					Node* Sibling = (*root)->C[goal_idx - 1];
					// ���� �׶���
					if (Sibling->N >= MIN_DEGREE)
					{
						// �����ž�
						// Target Ű �ڷ� �б�
						for (int i = Target->N; i >0; i--)
						{
							Target->Key[i] = Target->Key[i - 1];

						}
						// Target �ڽĵ� �б�
						for (int i = Target->N; i >= 0; i--)
						{
							Target->C[i + 1] = Target->C[i];
						}
						Target->Key[0] = (*root)->Key[goal_idx - 1];
						(*root)->Key[goal_idx - 1] = Sibling->Key[(Sibling->N) - 1];
						Target->C[0] = Sibling->C[Sibling->N];
						Sibling->N--;
						Target->N++;


					}
					// ���� �ȶ׶���
					else
					{
						// ��ĥ�ž�
						Sibling->Key[Sibling->N] = (*root)->Key[goal_idx-1];
						// Target�� ���� Sibling �� �����Ұž�
						for (int i = 0; i < Target->N; i++)
						{
							Sibling->Key[((Sibling->N) + 1) + i] = Target->Key[i];
						}
						for (int i = 0; i <= Target->N; i++)
						{
							Sibling->C[((Sibling->N) + 1) + i] = Target->C[i];
						}
						Sibling->N = Sibling->N + 1 + Target->N;
						free(Target);

						Target = Sibling;
						(*root)->N--;
						if ((*root)->N == 0)
						{
							//printf("root�� �ٲ�ϴ� \n");
							*root = Target;
						}
					}
				}
				// �� ��
				else
				{
					Node* Sibling = (*root)->C[goal_idx + 1];
					if (Sibling->N >= MIN_DEGREE)
					{
						// �����ž�
						Target->Key[Target->N] = (*root)->Key[goal_idx];
						Target->N++;
						// �ڽı��� ������.
						Target->C[(Target->N)] = Sibling->C[0];

						(*root)->Key[goal_idx] = Sibling->Key[0];

						// ������ Ű �� ����.
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];
						}
						
						// ������ C ����.
						for (int i = 0; i < Sibling->N; i++)
						{
							Sibling->C[i] = Sibling->C[i + 1];
						}
						Sibling->N--;
					}
					// ���� �ȶ׶���
					else
					{
						// ��ĥ�ž�
						// ������ �ƴϸ� �θ� �����ž�
						// ������ ������ ��ĥ ��, �θ� ������ �� �θ�� goal_idx�� �ִ�.
						Target->Key[Target->N] = (*root)->Key[goal_idx];
						for (int i = 0; i < Sibling->N; i++)
						{
							Target->Key[((Target->N) + 1) + i] = Sibling->Key[i];
						}

						for (int i = 0; i <= Sibling->N; i++)
						{
							Target->C[((Target->N) + 1) + i] = Sibling->C[i];
						}
						Target->N = Target->N + 1 + Sibling->N;


						for (int i = goal_idx - 1; i < ((*root)->N) - 1; i++)
						{

							(*root)->Key[i] = (*root)->Key[i + 1];
							(*root)->C[i + 1] = (*root)->C[i + 2];
						}
						(*root)->N--;
						if ((*root)->N == 0)
						{
							//printf("root�� �ٲ�ϴ� \n");
							*root = Target;
						}
						//free(Sibling);
						
					}
				}
			}
		}
		deleteTree(&Target, k);
	}

}