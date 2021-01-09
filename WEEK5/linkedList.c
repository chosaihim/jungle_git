#include <stdio.h>
#include <stdlib.h>     //malloc, free

typedef struct _NODE{
    struct _NODE *next;
    int data;
}NODE;

void addFirst(NODE *target, int data){

    NODE *newNode = malloc(sizeof(NODE));
    newNode->next = target->next;
    newNode->data = data;
    
    target->next = newNode;
}

void removeFirst(NODE *target){

    NODE *nextNode = target->next;

    target->next = nextNode->next;
    free(nextNode);  
}

int main(){

    //head: first node of the linked list
    NODE *head = malloc(sizeof(NODE));
    head->next = NULL;

    addFirst(head,10);
    addFirst(head,20);
    addFirst(head,30);

    removeFirst(head);

    NODE *curr = head->next;
    while (curr != NULL){
        printf("%d\n",curr->data);
        curr = curr-> next;
    }

    curr = head->next;
    while(curr != NULL){
        
        NODE *next = curr->next;
        free(curr);
        curr = next;
    }

    free(head);


    return 0;
}


