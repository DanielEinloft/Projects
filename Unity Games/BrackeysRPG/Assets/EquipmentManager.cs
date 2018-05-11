using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EquipmentManager : MonoBehaviour
{
    //singleton
    public static EquipmentManager instance;
    private void Awake()
    {
        instance = this;
    }


    Inventory inventory;
    Equipment[] currentEquipment;
    SkinnedMeshRenderer[] currentMashes;


    public delegate void OnEquipmentChange(Equipment newItem, Equipment oldItem);
    public OnEquipmentChange onEquipmentChange;
    public SkinnedMeshRenderer targetMash;
    public Equipment[] defaultItems;

    //equipa as roupas normais
    void EquipDefaultItems()
    {
        foreach(Equipment item in defaultItems)
        {
            Equip(item);
        }
    }


    private void Start()
    {
        //pega numero de elemtos de um enum
        int numSlots = System.Enum.GetNames(typeof(EquipmentSlot)).Length;
        inventory = Inventory.instance;
        currentEquipment = new Equipment[numSlots];
        currentMashes = new SkinnedMeshRenderer[numSlots];
        EquipDefaultItems();
    }

    public void Equip(Equipment newItem)
    {

        //descobre qual tipo de item (Head,Chest) e faz um cast (pois cada posicao do enum corresponde a uma posicao
        //de um vetor.Head = 0, chest = 1, etc. Pra ver isso, colocar omouse em cima dos items do enum.
        int slotIndex = (int)newItem.equipSlot;

        //tira item anterior
        Equipment oldItem = Unequip(slotIndex);
        SetEquipmentBlendShapes(newItem,100);

        //Equipment oldItem = null;
        ////se ja tem item equipado
        //if(currentEquipment[slotIndex] != null)
        //{
        //    oldItem = currentEquipment[slotIndex];
        //    Inventory.instance.Add(oldItem);
        //}

        if (onEquipmentChange != null)
            onEquipmentChange.Invoke(newItem, oldItem);

        currentEquipment[slotIndex] = newItem;

        //parte grafica
        SkinnedMeshRenderer newMesh = Instantiate<SkinnedMeshRenderer>(newItem.mesh);
        newMesh.transform.parent = targetMash.transform;

        //comportamento.
        newMesh.bones = targetMash.bones;
        newMesh.rootBone = targetMash.rootBone;
        currentMashes[slotIndex] = newMesh;


    }



    public Equipment Unequip(int slotIndex)
    {
        if(currentEquipment[slotIndex]!=null)
        {
            Equipment oldItem = currentEquipment[slotIndex];
            inventory.Add(oldItem);

            SetEquipmentBlendShapes(oldItem, 0);

            currentEquipment[slotIndex] = null;
            if (onEquipmentChange != null)
                onEquipmentChange.Invoke(null, oldItem);


            if (currentMashes[slotIndex] != null)
                Destroy(currentMashes[slotIndex].gameObject);


            return oldItem;
        }
        return null;
    }


    public void UnequipAll()
    {
        for (int i = 0; i < currentEquipment.Length; i++)
            Unequip(i);
        //coloca as roupas normais
        EquipDefaultItems();
    }

    void SetEquipmentBlendShapes(Equipment item, int weight)
    {

        foreach(EquipmentMeshRegion blendShape in item.coveredMashRegions)
        {
            targetMash.SetBlendShapeWeight((int)blendShape, weight);
        }
    }




    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.U))
            UnequipAll();
    }
}
