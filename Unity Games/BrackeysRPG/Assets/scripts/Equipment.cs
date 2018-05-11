using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName ="New Equipment", menuName ="Inventory/Equipment")]
public class Equipment : Item
{

    public EquipmentSlot equipSlot;
    public int amorModifier;
    public int damageModifier;
    public SkinnedMeshRenderer mesh;
    public EquipmentMeshRegion[] coveredMashRegions;

    public override void Use()
    {
        base.Use();

        //equip item
        EquipmentManager.instance.Equip(this);
        RemoveFromInventory();
        //remove from inventory
    }


}



public enum EquipmentSlot { Head, Chest, Legs, Weapon, Shield, Feet}
public enum EquipmentMeshRegion { Legs, Arms, Torso}//pra nao dar erro (pedaçosda pele pra fora xP)com a sessao "blendshapes" do Player/body. 