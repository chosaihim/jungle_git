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
	// 삽입과정에서 필요하여, 하나씩 더 추가
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
	
	// 리프가 아니면
	if (!root->isLeaf)
		return searchNode(root->C[idx], k);

	else
	{
		idx--;
		// 찾았어
		if ((idx >= 0) && k == root->Key[idx])
			return 1;
		// 못찾았어
		else
			return 0;
	}
	
}


void insertTree(Node** root, int k)
{


		Node* tmp = *root;
		if (((*root)->N == MAX_DEGREE))
		{
			// 루트가 될 노드 생성
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
		// 내가 들어갈 공간 위에 서있어
		idx++;

		// 내가 들어갈 자녀들이 가득 찼으면
		if (root->C[idx]->N == MAX_DEGREE)
		{
			splitChild(root, idx);
			// split 후 root에 값이 추가되니까 내가 어디로 들어갈 지 다시 확인
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
	//******************개수 설정해줘야함************************
	//right->N = MIN_DEGREE - 1;

	// 찢을 놈이 리프일때, 부모한테 복사해서 올려줌 (copy up)
	if (left->isLeaf)
	{

		right->Next = left->Next;
		left->Next = right;
		// 오른쪽에 왼쪽의 뒷값들을 넣어주고
		for (int i = 0; i < MIN_DEGREE - 1; i++)
		{
			// 왼쪽이 뚱뚱해짐
			right->Key[i] = left->Key[i + MIN_DEGREE];
			// 리프와, 내부 노드 모드 C(자녀)들을 갖는다.
		}

		// 다음 노드를 가리키게 연결
		right->N = MIN_DEGREE - 1;
		left->N = MIN_DEGREE;


		//(부모) 밀고, 중간자를 올리고, 자식 연결시키고
		// 자식 올라갈 녀석 자리 마련
		// idx N 이면, parent-> N : N-1, idx : N 이라서 for문이 돌지 않음!
		for (int i = parent->N; i >= idx; i--)
		{
			parent->C[i + 1] = parent->C[i];
		}
		// idx가 N이어도, 값이 추가되니까
		parent->C[idx + 1] = right;
		// 키 올라갈 녀석 자리 마련
		for (int i = parent->N - 1; i >= idx; i--)
		{
			parent->Key[i + 1] = parent->Key[i];
		}
		// 부모에 키 삽입
		parent->Key[idx] = right->Key[0];
		parent->N++;

	}

	//리프가 아니면, (B TREE 와 동일 )
	else
	{
		// 오른쪽에 왼쪽의 뒷값들을 넣어주고
		for (int i = 0; i < MIN_DEGREE - 1; i++)
		{
			// 왼쪽이 뚱뚱해짐
			right->Key[i] = left->Key[i + MIN_DEGREE];
		}
		// 리프와, 내부 노드 모드 C(자녀)들을 갖는다.
		for (int i = 0; i < MIN_DEGREE; i++)
		{
			right->C[i] = left->C[i + MIN_DEGREE];
		}

		left->N = MIN_DEGREE - 1;
		right->N = MIN_DEGREE - 1;

		// 자식 올라갈 녀석 자리 마련
		// idx N 이면, parent-> N : N-1, idx : N 이라서 for문이 돌지 않음!
		for (int i = parent->N; i >= idx; i--)
		{
			parent->C[i + 1] = parent->C[i];
		}
		// idx가 N이어도, 값이 추가되니까
		parent->C[idx + 1] = right;
		// 키 올라갈 녀석 자리 마련
		for (int i = parent->N - 1; i >= idx; i--)
		{
			parent->Key[i + 1] = parent->Key[i];
		}
		// 부모에 키 삽입
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

		printf("\t다음 자식은 : %p", node->Next);
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

	// 안에 없을 때만 삭제 시작

	int idx = (*root)->N;

	// 나보다 다 크면, 0에 서게 됨
	// 내가 제일 크면 N에 서있음
	while (idx > 0 & (*root)->Key[idx - 1] > k)
	{
		idx--;
	}

	const int goal_idx = idx;

	// 들어온 너 리프야?
	if ((*root)->isLeaf)
	{
		// 나는 Key[goal_idx - 1]이다.
		for (int i = goal_idx - 1; i < ((*root)->N) - 1; i++)
		{
			(*root)->Key[i] = (*root)->Key[i + 1];
		}
		(*root)->N--;
	}
	// 리프아니야 ( == 나 더 들어갈 수 있어 !!)
	else
	{
		Node* Target = (*root)->C[goal_idx];
		if (Target->N < MIN_DEGREE)
		{
			// 자식이 안뚱뚱한데, 리프야
			if (Target->isLeaf)
			{
				// 오른쪽 끝에 서있으면, 무조건 왼쪽 형제가 형제다.
				if (goal_idx == (*root)->N)
				{
					// 빌려온다 -> 끝값을 빌려오고, 부모를 업데이트 해줘야함
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
						// 합친다.
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
							//printf("\nroot가 바뀝니다 \n");
							*root = Target;
						}
					}

				}

				// 그 외에는, 무조건 오른쪽 형제가 형제다.
				else
				{
					Node* Sibling = (*root)->C[goal_idx + 1];
					// 형제 뚱뚱해 ? -> 빌려올거야
					if (Sibling->N >= MIN_DEGREE)
					{
						Target->Key[Target->N] = (*root)->Key[goal_idx];
						Target->N++;
						// 끝 Child 에 Sibling 연결시켜준다.

						// 형제의 키 값 당긴다.
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];

						}
						Sibling->N--;
						(*root)->Key[goal_idx] = Sibling->Key[0];
					}
					// 형제도 안뚱뚱해 -> 합칠거야
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
							//printf("\nroot가 바뀝니다 \n");
							*root = Target;
						}
						//free(Sibling);
					}
				}
			}
			// 자식이 안뚱뚱한데, 리프가 아니야
			else
			{
				// 오른쪽 끝에 서있다.
				if (goal_idx == (*root)->N)
				{
					Node* Sibling = (*root)->C[goal_idx - 1];
					// 형제 뚱뚱해
					if (Sibling->N >= MIN_DEGREE)
					{
						// 빌릴거야
						// Target 키 뒤로 밀기
						for (int i = Target->N; i >0; i--)
						{
							Target->Key[i] = Target->Key[i - 1];

						}
						// Target 자식들 밀기
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
					// 형제 안뚱뚱해
					else
					{
						// 합칠거야
						Sibling->Key[Sibling->N] = (*root)->Key[goal_idx-1];
						// Target의 값을 Sibling 에 복사할거야
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
							//printf("root가 바뀝니다 \n");
							*root = Target;
						}
					}
				}
				// 그 외
				else
				{
					Node* Sibling = (*root)->C[goal_idx + 1];
					if (Sibling->N >= MIN_DEGREE)
					{
						// 빌릴거야
						Target->Key[Target->N] = (*root)->Key[goal_idx];
						Target->N++;
						// 자식까지 보낸다.
						Target->C[(Target->N)] = Sibling->C[0];

						(*root)->Key[goal_idx] = Sibling->Key[0];

						// 형제의 키 값 당긴다.
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];
						}
						
						// 형제의 C 당긴다.
						for (int i = 0; i < Sibling->N; i++)
						{
							Sibling->C[i] = Sibling->C[i + 1];
						}
						Sibling->N--;
					}
					// 형제 안뚱뚱해
					else
					{
						// 합칠거야
						// 리프가 아니면 부모도 넣을거야
						// 오른쪽 형제와 합칠 때, 부모를 내리면 그 부모는 goal_idx에 있다.
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
							//printf("root가 바뀝니다 \n");
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