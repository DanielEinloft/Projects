using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InventoryUI : MonoBehaviour
{
    public Transform itemsParent;
    public GameObject inventoryUI;

    Inventory inventory;
    InventorySlot[] slots;


    void Start ()
    {
        inventory = Inventory.instance;
        //usa o delegate pra chamar funcoes. Neste caso, vaiatualizar a interface quando esta funcao for chamada (qualquer um que executar vai chamar esta funcao)
        //ja esta sendo chamado quando clica num item
        inventory.onItemChangedCallback += UpdateUI;


        slots = itemsParent.GetComponentsInChildren<InventorySlot>();
	}
	

    void UpdateUI()
    {
        Debug.Log("Updateing UUI");
        for(int i = 0;i <slots.Length;i++)
        {
            //more items to add?
            if (i < inventory.items.Count)
            {
                slots[i].AddItem(inventory.items[i]);
            }
            else
                slots[i].ClearSlot();
        }
    }
	// Update is called once per frame
	void Update ()
    {
        if (Input.GetButtonDown("Inventory"))
        {
            inventoryUI.SetActive(!inventoryUI.activeSelf);
        }

    }
}
