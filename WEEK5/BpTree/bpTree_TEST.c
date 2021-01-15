#include <stdio.h>
#include <stdbool.h>

#define DEGREE 4
#define TEST { 10,1,3,63,82,6,31,8,2,16,11,77,96,14,92,21,47,23,24,78,26,97,15,4,30,69,37,38,76,90,17,87,53,44,45,46,9,41,54,43,22,84,58,39,65,28,42,59,99,70,71,72,29,74,73,68,13,60,79,80,81,85,83,64,94,86,66,88,93,40,91,62,25,20,36,95,19,52,55,100 }



int MIN_DEGREE = (int)(DEGREE / 2);
int MAX_DEGREE = DEGREE - 1;

typedef struct _NODE
{
	struct _NODE** C;
	struct _NODE* Right;
	int* Key;
	int N;
	bool isLeaf;

}Node;


Node* createNode();
void Traverse(Node* root, int depth);
void insertTree(Node** root, int k, int data);
void insertNonfull(Node* root, int k, int data);
void splitNode(Node* root, int idx);
void deleteNode(Node** root, int k);
int searchNode(Node* root, int k);
void print_for_exam(Node* root);


int main()
{
	Node* root = createNode();
	root->N = 0;
	root->isLeaf = true;
	int arr[80] = TEST;


	// TEST 1 CASE


	insertTree(&root, 4, 4 * 1000);
	insertTree(&root, 1, 1 * 1000);
	insertTree(&root, 3, 3 * 1000);
	insertTree(&root, 2, 2 * 1000);
	deleteNode(&root, 4);
	deleteNode(&root, 2);
	deleteNode(&root, 3);



	printf("---- TEST1 ----\n");
	print_for_exam(root);

	// TEST 2 CASE
	for (int i = 2; i <= 100; i++) {
		if (!searchNode(root, i))
			insertTree(&root, i, i * 1000);
	}

	for (int i = 50; i <= 70; i++) {
		if (searchNode(root, i))
			deleteNode(&root, i);
		//Traverse(root, 0);
	}
	printf("---- TEST2 ----\n");
	print_for_exam(root);

	// TEST3 CASE
	for (int i = 50; i <= 70; i++) {
		if (!searchNode(root, i))
			insertTree(&root, i, i * 1000);

	}

	for (int i = 0; i < 80; i++) {
		if (searchNode(root, arr[i]))
			deleteNode(&root, arr[i]);

	}

	printf("\n\n\n\n\n\n");
	printf("---- TEST3 ----\n");

	print_for_exam(root);
	printf("프로그램이 정상적으로 종료 되었음.");



	return 0;
}


Node* createNode()
{
	Node* newNode = (Node*)malloc(sizeof(Node));
	Node** children = (Node**)malloc((DEGREE + 1) * sizeof(Node*));
	int* key = (int*)malloc(DEGREE * sizeof(int));
	newNode->C = children;
	newNode->Key = key;
	newNode->Right = NULL;

	return newNode;
}

void Traverse(Node* root, int depth)
{
	if (root->isLeaf)
	{
		for (int i = 0; i < depth; i++)
		{
			printf("\t\t\t||");
		}
		for (int i = 0; i < root->N; i++)
		{
			printf("%6d", root->Key[i]);
		}
		printf("\tNext : %p\n", root->Right);
		return;
	}

	if (!root->isLeaf)
	{
		for (int i = 0; i < depth; i++)
		{
			printf("\t\t\t||");
		}
		for (int i = 0; i < root->N; i++)
		{
			printf("%6d", root->Key[i]);
		}
		printf("\n");
		for (int i = 0; i <= root->N; i++)
		{
			Traverse(root->C[i], depth + 1);
		}
	}
}

void insertTree(Node** ptr_root, int k, int data)
{
	Node* root = *ptr_root;

	// ONLY for ROOT
	// bc the other NODES is already skinny BEFORE insert
	if (root->N == MAX_DEGREE)
	{
		// UPDATE root
		Node* newRoot = createNode();
		*ptr_root = newRoot;

		newRoot->isLeaf = false;
		newRoot->N = 0;
		newRoot->C[0] = root;

		splitNode(newRoot, 0);
		insertNonfull(newRoot, k, data);
	}
	else
	{
		insertNonfull(root, k, data);
	}
}
void insertNonfull(Node* root, int k, int data)
{

	// for Leaf
	if (root->isLeaf)
	{
		// Find my loc & Push
		int idx = root->N;
		while (idx > 0 && root->Key[idx - 1] >= k)
		{
			root->Key[idx] = root->Key[idx - 1];
			idx--;
		}
		root->Key[idx] = k;
		root->C[idx] = data;
		root->N++;
	}

	// for Internal Node
	else
	{
		// FIND Target idx
		int idx = root->N;
		// "이하" 이기 때문에 "너 나보다 크거나 같아?"
		while (idx > 0 && root->Key[idx - 1] >= k)
		{
			idx--;
		}
		Node* Target = root->C[idx];
		// for FULL Target - SPLIT
		if (Target->N == MAX_DEGREE)
		{
			splitNode(root, idx);
			// Check value in idx After Split
			if (k > root->Key[idx])
			{
				idx++;
				// update Target
				Target = root->C[idx];
			}
		}
		// now go into the Target
		insertNonfull(Target, k, data);
	}
}
void splitNode(Node* root, int idx)
{
	Node* Target = root->C[idx];
	// it would be the error cause last code
	Node* Empty_Right = createNode();
	Empty_Right->isLeaf = Target->isLeaf;

	// Push Root Key
	for (int i = root->N; i > idx; i--)
	{
		// push same times
		// bc I will add newRoot
		root->Key[i] = root->Key[i - 1];
		root->C[i + 1] = root->C[i];
	}

	// Leaf split -> copy up
	if (Target->isLeaf)
	{
		// save Address
		Empty_Right->Right = Target->Right;
		Target->Right = Empty_Right;

		// copy to right
		for (int i = 0; i < (MIN_DEGREE - 1); i++)
		{
			Empty_Right->Key[i] = Target->Key[MIN_DEGREE + i];
			Empty_Right->C[i] = Target->C[MIN_DEGREE + i];
		}
		Empty_Right->N = MIN_DEGREE - 1;
		Target->N = MIN_DEGREE;

		// Predecessor will be Parent's Key
		root->Key[idx] = Target->Key[Target->N - 1];
		root->C[idx + 1] = Empty_Right;
		root->N++;
	}
	// Internal split -> push up

	else
	{
		// Target Boundary will be Parent's Key
		root->Key[idx] = Target->Key[MIN_DEGREE - 1];
		root->N++;
		root->C[idx + 1] = Empty_Right;

		// push Key
		for (int i = 0; i < (MIN_DEGREE - 1); i++)
		{
			Empty_Right->Key[i] = Target->Key[MIN_DEGREE + i];
		}
		// push Children
		for (int i = 0; i < MIN_DEGREE; i++)
		{
			Empty_Right->C[i] = Target->C[MIN_DEGREE + i];
		}
		Empty_Right->N = MIN_DEGREE - 1;
		Target->N = MIN_DEGREE - 1;
	}
}

void deleteNode(Node** ptr_root, int k)
{
	Node* root = *ptr_root;

	// for Leaf
	if (root->isLeaf)
	{
		for (int i = 0; i < (root->N) - 1; i++)
		{
			// don't need to check last one, bc thats mine
			if (root->Key[i] < k)
				continue;
			// after meeting myself
			else if (root->Key[i] >= k)
			{
				root->Key[i] = root->Key[i + 1];
				root->C[i] = root->C[i + 1];
			}
		}
		// 나 끝에 서있으면 개수만 줄이면 돼
		root->N--;
	}
	else
	{
		// find Target
		int idx = root->N;
		while (idx > 0 && root->Key[idx - 1] >= k)
		{
			idx--;
		}
		Node* Target = root->C[idx];
		// is Target Not Enough? -> Make it FULL
		if (Target->N < MIN_DEGREE)
		{
			// define Sibling
			Node* Sibling;

			// is Nonfull target Leaf?
			if (Target->isLeaf)
			{
				// NO Right Sibling ( on right end )
				if (idx == root->N)
				{
					Sibling = root->C[idx - 1];
					// borrow
					if (Sibling->N >= MIN_DEGREE)
					{
						// push target key
						for (int i = Target->N; i > 0; i--)
						{
							Target->Key[i] = Target->Key[i - 1];
							// data push
							Target->C[i] = Target->C[i - 1];
						}
						Target->Key[0] = Sibling->Key[(Sibling->N) - 1];
						Target->N++;
						Sibling->N--;
						root->Key[idx - 1] = Sibling->Key[(Sibling->N) - 1];

					}
					// merge
					else
					{
						for (int i = 0; i < Target->N; i++)
						{
							Sibling->Key[(Sibling->N) + i] = Target->Key[i];
							Sibling->C[(Sibling->N) + i] = Target->C[i];
						}
						Sibling->N = Sibling->N + Target->N;
						//free(Target);
						Target = Sibling;
						Target->Right = NULL;
						// pull root
						root->N--;
						if (root->N == 0)
						{
							*ptr_root = Target;
						}

					}

				}
				// has Right Sibling
				else
				{
					Sibling = root->C[idx + 1];
					// borrow
					if (Sibling->N >= MIN_DEGREE)
					{
						Target->Key[Target->N] = Sibling->Key[0];
						Target->C[Target->N] = Sibling->C[0];
						Target->N++;
						root->Key[idx] = Target->Key[(Target->N) - 1];
						// pull Sibling Key
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];
							Sibling->C[i] = Sibling->C[i + 1];
						}
						Sibling->N--;
					}
					// merge
					else
					{
						for (int i = 0; i < Sibling->N; i++)
						{
							Target->Key[(Target->N) + i] = Sibling->Key[i];
							Target->C[(Target->N) + i] = Sibling->C[i];
						}
						Target->Right = Sibling->Right;
						Target->N = Target->N + Sibling->N;

						// pull parent's key & children
						// from myself
						for (int i = idx; i < (root->N) - 1; i++)
						{
							// root->Key[idx+1]로 교체됨 : 지움
							root->Key[i] = root->Key[i + 1];
							root->C[i + 1] = root->C[i + 2];
						}
						//free(Sibling);
						root->N--;
						if (root->N == 0)
						{
							*ptr_root = Target;
						}
					}

				}
			}
			// is Nonfull target Internal? 
			else
			{
				// NO Right Sibling
				if (idx == root->N)
				{
					Sibling = root->C[idx - 1];
					// borrow with parent's key
					if (Sibling->N >= MIN_DEGREE)
					{
						// push target Key
						for (int i = (Target->N); i > 0; i--)
						{
							Target->Key[i] = Target->Key[i - 1];
						}
						// push childeren
						for (int i = (Target->N) + 1; i > 0; i--)
						{
							Target->C[i] = Target->C[i - 1];
						}

						// idx에는 키가 없었다!!!!!
						Target->Key[0] = root->Key[idx - 1];
						Target->C[0] = Sibling->C[Sibling->N];
						Target->N++;
						root->Key[idx - 1] = Sibling->Key[(Sibling->N) - 1];
						Sibling->N--;
					}
					// merge
					else
					{
						// merge with parent
						// root의 idx 에는 키가 없다!!
						Sibling->Key[(Sibling->N)] = root->Key[idx - 1];
						for (int i = 0; i < Target->N; i++)
						{
							Sibling->Key[((Sibling->N) + 1) + i] = Target->Key[i];
						}
						for (int i = 0; i <= Sibling->N; i++)
						{
							Sibling->C[((Sibling->N) + 1) + i] = Target->C[i];
						}
						Sibling->N = Sibling->N + 1 + Target->N;

						free(Target);
						Target = Sibling;
						root->N--;
						if (root->N == 0)
						{
							*ptr_root = Target;
						}
					}
				}
				// Has Right Sibling
				else
				{
					Sibling = root->C[idx + 1];
					// borrow with parent's key
					if (Sibling->N >= MIN_DEGREE)
					{
						Target->Key[Target->N] = root->Key[idx];
						Target->N++;
						// patch Child
						Target->C[Target->N] = Sibling->C[0];
						root->Key[idx] = Sibling->Key[0];
						// pull Sibling's key
						for (int i = 0; i < (Sibling->N) - 1; i++)
						{
							Sibling->Key[i] = Sibling->Key[i + 1];
						}
						// pull Sibling's children
						for (int i = 0; i < Sibling->N; i++)
						{
							Sibling->C[i] = Sibling->C[i + 1];
						}
						Sibling->N--;
					}
					//merge
					else
					{
						// merge with parent
						Target->Key[(Target->N)] = root->Key[idx];
						for (int i = 0; i < Sibling->N; i++)
						{
							Target->Key[((Target->N) + 1) + i] = Sibling->Key[i];
						}
						for (int i = 0; i <= Sibling->N; i++)
						{
							Target->C[((Target->N) + 1) + i] = Sibling->C[i];
						}
						Target->N = Target->N + 1 + Sibling->N;

						// from myself
						for (int i = idx; i < (root->N) - 1; i++)
						{
							root->Key[i] = root->Key[i + 1];
							root->C[i + 1] = root->C[i + 2];
						}
						root->N--;
						if (root->N == 0)
						{
							*ptr_root = Target;
						}
						//free(Sibling);
					}
				}
			}

		}
		deleteNode(&Target, k);
	}
}


int searchNode(Node* root, int k)
{
	int idx = (root->N);
	while (idx > 0 && root->Key[idx - 1] >= k)
	{
		idx--;
	}

	// if not root
	if (!root->isLeaf)
		return searchNode(root->C[idx], k);

	else
	{
		// find it
		if ((idx >= 0) && k == root->Key[idx])
			return 1;
		// can't find
		else
			return 0;
	}

}

void print_for_exam(Node* root) {
	if (root->isLeaf) {
		for (int i = 0; i < root->N; i++) {
			printf("[%5d, %5d]\n", root->Key[i], root->C[i]);
		}
	}
	else {
		for (int i = 0; i < root->N; i++) {
			print_for_exam(root->C[i]);
			printf("[%5d]\n", root->Key[i]);
		}
		print_for_exam(root->C[root->N]);
	}
}
