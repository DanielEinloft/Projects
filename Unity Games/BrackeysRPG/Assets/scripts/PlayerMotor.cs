using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;


//garante que sempre tenha um componente navmeshagent

[RequireComponent(typeof(NavMeshAgent))]
public class PlayerMotor : MonoBehaviour
{

    Transform target;
    NavMeshAgent agent;
    


    void Start ()
    {
        agent = GetComponent<NavMeshAgent>();
	}

    //mudar a posicao algumas x por segundo, usar co rotina, pra melhorar o desempenho
    private void Update()
    {
        //quando existe um alvo, fica repetindo a destination e face
        //é importane que isso esteja no update (ou numa co rotina) e não numa das funcoes ali de baixo pq
        //caso o objeto alvo se mexer, o set destination e olhar pro alvo tem que se mexer também
        //caso contrário isso so seria executado quando a funcao ali em baixo for chamada 
        // (e elas só são chamadas no playerController quando acontece um evento de click)
        if(target!= null)
        {
            agent.SetDestination(target.position);
            FaceTarget();
        }
    }


    public void MoveToPoint(Vector3 point)
    {
        agent.SetDestination(point);
    }

    public void FollowTarget(Interactable newTarget)
    {
        //0.8f pra  parar quase ali na borda
        agent.stoppingDistance = newTarget.radius * .8f;
        //target = newTarget.transform;
        target = newTarget.interactionTransform; 
        //a rotação só muda quando o objeto sair desse raio. Então é necessário setar isso manualmente
        agent.updateRotation = false;
        
    }
    
    public void StopFollowingTarget()
    {
        target = null;
        agent.stoppingDistance = 0f;

        //tem que setar pra true pois agora que nao tem objeto pra ver, a rotação volta ao normal.
        agent.updateRotation = true;
    }

    void FaceTarget()
    {
        Vector3 direction = (target.position - transform.position).normalized;
        //coloca 0 no y pra não ficar olhando pra cimae pra baixo 
        Quaternion lookRotation = Quaternion.LookRotation(new Vector3(direction.x, 0, direction.z));
        //Slerp é um lerp so que quartenion:P
        transform.rotation = Quaternion.Slerp(transform.rotation, lookRotation, Time.deltaTime * 5f);

    }


}
