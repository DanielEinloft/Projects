using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class characterAnimator : MonoBehaviour
{

    Animator animator;
    NavMeshAgent agent;    //pra pegar a velocidade atual do agente

    const float locomotioAnimationSmoothTime = .1f; // 1/10 segundo de smooth

    void Start ()
    {
        agent = GetComponent<NavMeshAgent>();
        animator = GetComponentInChildren<Animator>();
	} 
	
	// Update is called once per frame
	void Update ()
    {
        //velocity é um vetor, por isso é importante pegar a magnitude. É de 0 a 1
        //speed é a velocidade máxima
        float speedPercent = agent.velocity.magnitude / agent.speed;
        animator.SetFloat("speedPercent",speedPercent, locomotioAnimationSmoothTime, Time.deltaTime);
	}
}
