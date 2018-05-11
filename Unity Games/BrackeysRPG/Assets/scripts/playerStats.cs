using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class playerStats : CharacterStats
{

	// Use this for initialization
	void Start ()
    {
        EquipmentManager.instance.onEquipmentChange += onEquipmentChanged;
	}
	
    void onEquipmentChanged(Equipment newItem, Equipment oldItem)
    {
        if (newItem != null)
        {
            armor.AddModifier(newItem.amorModifier);
            damage.AddModifier(newItem.damageModifier);
        }

        if(oldItem!= null)
        {
            armor.RemoveModifier(oldItem.amorModifier);
            damage.RemoveModifier(oldItem.damageModifier);
        }
    }

    public override void Die()
    {
        base.Die();
        //kill player :O
        PlayerManager.instance.KillPlayer();
    }

}
