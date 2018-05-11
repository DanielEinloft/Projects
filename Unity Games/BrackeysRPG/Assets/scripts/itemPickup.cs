using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class itemPickup : Interactable
{
    //Item -> Scriptable objetct definido em Item.cs
    public Item item;



    //substitui o método interact
    public override void Interact()
    {
        //pra acessar o método pai
        base.Interact();

        Pickup();
    }

     void Pickup()
    {

        Debug.Log("Picking Up "+ item.name);

        //add item to inventory
        

        bool wasPickedUp = Inventory.instance.Add(item);

        if(wasPickedUp)
            Destroy(gameObject);


    }

}
