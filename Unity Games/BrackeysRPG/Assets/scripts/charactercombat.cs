using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(CharacterStats))]
public class charactercombat : MonoBehaviour {

    CharacterStats myStats;
    public float attackspeed = 1f;
    private float attackCooldown = 0f;

    //é tipo um delegate sem argumento e void
    public event System.Action OnAttack;

    private void Start()
    {
        myStats = GetComponent<CharacterStats>();
    }
    public void Attack(CharacterStats targeStats)
    {
        if (attackCooldown <= 0f)
        {
            StartCoroutine(DoDamage(targeStats, 0.6f));
            if (OnAttack != null)
                OnAttack();
            attackCooldown = 1f / attackspeed;
        }
    }

    private void Update()
    {
        attackCooldown -= Time.deltaTime;
    }

    IEnumerator DoDamage(CharacterStats stats, float delay)
    {
        yield return new WaitForSeconds(delay);
        stats.TakeDamage(myStats.damage.GetValue());

    }

}
