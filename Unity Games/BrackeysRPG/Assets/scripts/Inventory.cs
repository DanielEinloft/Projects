using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public List<Item> items = new List<Item>();

    public int space = 20;


    //evento que tu pode adicionar diferentes métodos. Quando dá um trigger no evento, todos os eventos
    //aka funções adicionadas sao executadas.
    public delegate void OnItemChange();
    public OnItemChange onItemChangedCallback;



    //pelo que eu entendi ele define um inventório só pra todo mundo (pra parte estatica, no caso)
    //dessa forma nao precisa ficar chamando "getcomponnetofinstance..", pq so existe um inventorio.
    //basicamente define UM inventório global, que vai ser usado no game manager. :)
    public static Inventory instance;
    private void Awake()
    {
        if(instance != null)
        {
            Debug.LogWarning("More than one instance of inventory found");
        }
        instance = this;
    }





    public bool Add(Item item)
    {
        if (!item.isDefaultItem)
        {
            if (items.Count >= space)
            {
                Debug.Log("Not enough space!");
                return false;
            }
            items.Add(item);

            //isso vai ser utilizado para a interface dar update 
            if(onItemChangedCallback!=null)
                onItemChangedCallback.Invoke();
        }
 
        return true;
    }

    public void Remove(Item item)
    {
        items.Remove(item);

        //isso vai ser utilizado para a interface dar update 
        if (onItemChangedCallback != null)
            onItemChangedCallback.Invoke();
    }
}
