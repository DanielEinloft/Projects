﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class EnemyController : MonoBehaviour
{


    public float lookRadius = 10f;
    Transform target;
    NavMeshAgent agent;
    charactercombat combat;

    
    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, lookRadius);

    }
    // Use this for initialization
    void Start ()
    {
        agent = GetComponent<NavMeshAgent>();
        //usa o playermanager pra não ter que procurar a tag entre todos os objetos.
        target = PlayerManager.instance.player.transform;
        combat = GetComponent<charactercombat>();
	}
	
    void FaceTarget()
    {
        Vector3 direction = (target.position - transform.position).normalized;
        Quaternion lookRotation = Quaternion.LookRotation(new Vector3(direction.x, 0, direction.y));
        transform.rotation = Quaternion.Slerp(transform.rotation, lookRotation, Time.deltaTime * 5f);//lookRotation;
    }
	// Update is called once per frame
	void Update ()
    {
        float distance = Vector3.Distance(target.position, transform.position);

        if(distance <= lookRadius)
        {
            agent.SetDestination(target.position);
            if(distance <= agent.stoppingDistance)
            {
                CharacterStats targetStats = target.GetComponent<CharacterStats>();
                if(targetStats !=null)
                    combat.Attack(targetStats);


                FaceTarget();
            }
        }
	}
}
