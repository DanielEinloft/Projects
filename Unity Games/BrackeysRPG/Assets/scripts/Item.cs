using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//como criar novos items? Adicionando esta linha, adiciona a possibilidade de criar itens de forma um pouco mais dinâmica, sem a
//necessidade de ficar criando 300 prefabs. Pra ver isso direitinho, clica com botão direitonos assets, vai em criar e vai ver
//que existe um asset chamado Inventory e item dentro. Criando ele, vai criar um oobjeto do tipo Item com nome e icone :)
[CreateAssetMenu(fileName = "New Item", menuName = "Inventory/Item")]

//BLUEPRINT para items!!!!!!
public class Item : ScriptableObject
{

    //override a definicao "name" antiga de name pq ja tem xP, por isso usar new
    new public string name = "New Item";
    public Sprite icon = null;
    public bool isDefaultItem = false;


    public virtual void Use()
    {
        //virtual method for different items
        Debug.Log("Using " + name);
    }

    public void RemoveFromInventory()
    {
        Inventory.instance.Remove(this);
    }


}
