using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(CharacterStats))]
public class Enemy : Interactable
{

    CharacterStats myStats;

    private void Start()
    {
        myStats = GetComponent<CharacterStats>();
    }
    public override void Interact()
    {
        base.Interact();
        //attack
        charactercombat playerCombat =  PlayerManager.instance.player.GetComponent<charactercombat>();
        if(playerCombat != null)
        {
            playerCombat.Attack(myStats);
        }
    }

}
