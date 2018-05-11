using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CharacterStats : MonoBehaviour
{
    public int MaxHealth = 100;
    public int currentHealth { get; private set; }
    public Stat damage;
    public Stat armor;

    private void Awake()
    {
        currentHealth = MaxHealth;
    }

    public void TakeDamage(int damage)
    {
        damage -= armor.GetValue();

        //pra nao ir menos de 0
        damage = Mathf.Clamp(damage, 0, int.MaxValue);

        currentHealth -= damage;
        Debug.Log(transform.name + " takes " + damage + " damage");

        if (currentHealth < 0)
            Die();

    }

    private void Update()
    {
        if(Input.GetKeyDown(KeyCode.T))
        {
            TakeDamage(10);
        }
    }
    public virtual void Die()
    {
        //die in somw way
        //meant to be overritten

    }
}
