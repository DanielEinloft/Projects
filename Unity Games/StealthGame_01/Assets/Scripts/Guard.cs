using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Guard : MonoBehaviour {



    public static event System.Action OnGuardHasSpottedPlayer; //funcao sem parametros 


    [Header("Game Objects")]
    public Transform pathHolder;
    public Light spotlight;

    [Header("Controle Variables")]
    public float Speed = 5;
    public float waitTime = 0.5f;
    public float turnSpeed = 90; //90 graus por segundo.
    public float viewDistance;
    public LayerMask viewMask;
    public float timeToSpotPlayer = 0.5f;
    
    private float viewAngle;
    private Transform player;
    private Color originalColor;
    private float playerVisibleTimer;



    private void Start()
    {

        player = GameObject.FindGameObjectWithTag("Player").transform;
        originalColor = spotlight.color;
        viewAngle = spotlight.spotAngle;

        //aray de posicoes do waypoint
        Vector3[] waypoints = new Vector3[pathHolder.childCount];
        for (int i = 0; i < waypoints.Length; i++)
        {
            waypoints[i] = pathHolder.GetChild(i).position;
            waypoints[i] = new Vector3(waypoints[i].x, transform.position.y, waypoints[i].z);
        }

        //Comeca a routina followpath com os waypoints carregados.
        StartCoroutine(FollowPath(waypoints));
        //StartCoroutine(FollowPlayer());

    }

    //para desenhar icones dos inimigos. 
    private void OnDrawGizmos()
    {
        //pega a posicao do primeiro waypoint (Waypoint1)..
        Vector3 startPosition = pathHolder.GetChild(0).position;
        // e coloca na 1a posicao do loop
        Vector3 previousPOsition = startPosition;

       foreach(Transform waypoint in pathHolder)
       {
            //para eles aparecerem na camera vai em togglegizmoson no inspector.
            Gizmos.DrawSphere(waypoint.position, 0.3f);
            //desenha uma linha da posicao anterior ate a posicao do waypoint atual.
            Gizmos.DrawLine(previousPOsition, waypoint.position);
            //atualiza posicao anterior para o proximo desenho
            previousPOsition = waypoint.position;
       }
        Gizmos.DrawLine(previousPOsition, startPosition);

        Gizmos.color = Color.red;
        Gizmos.DrawRay(transform.position, transform.forward * viewDistance);

    }


    




    bool canSeePlayer()
    {
        //IMPORTANTE: CRIAR UM LAYER CHAMADO "OBSTACLE" E NOS OBSTACULOS COLOCAR NESTE LAYER. ADICIONAR OBSTACLE NO VIEW MASK DO GUARDA

        //analisa se ta numa distancia valida
        if (Vector3.Distance(transform.position,player.position) < viewDistance)
        {            
            //direcao do player e obstaculo
            Vector3 dirToPlayer = (player.position - transform.position).normalized; //distancia player e guarda
            float angleBetweenGuardAndPlayer = Vector3.Angle(transform.forward, dirToPlayer); //MENOR angulo entre os dois


            //se estiver dentro do angulo (dividido por dois pq se ficar do lado do guarda, conta 90 graus. como o angulo de vista é -45 ~ 45, precisa ser dividido por 2)
            if (angleBetweenGuardAndPlayer < viewAngle/2f)
            {

                // joga um raio entre dois pontos. Se atinge,alright:) (ver oque faz linecast)
                //garante que um objeto na frente impede que o jogador seja detectado. Utilizar isto para enchergar acima de caixas, etc 
                if (!Physics.Linecast(transform.position, player.position,viewMask))
                {
                    return true;
                }
            }
        }
        return false;
    }



    IEnumerator FollowPlayer()
    {
        while(true)
        {
            transform.LookAt(player.position);
            transform.position = Vector3.MoveTowards(transform.position, player.position, Speed * Time.deltaTime);
            yield return null;
        }

        
    }


    //desenhos mais claros no caderninho do lego com titulo "GUARDA OLHAR SUAVEMENTE PARA ALVO"
    IEnumerator TurnToFace(Vector3 lookTarget)
    {
        //faz a diferenca da posicao target e local e normaliza (valores de 0~1)
        Vector3 dirToLookTarget = (lookTarget - transform.position).normalized;
        //atan2(z/x) -> angulo entre valores z e x. Diminui de 90 graus pq 90 graus ( |_ ) significa que o objeto esta na frente. 
        float targetAngle = 90 - Mathf.Atan2(dirToLookTarget.z, dirToLookTarget.x) * Mathf.Rad2Deg;


        //se a diferenca de angulos ao redor do y (ou seja, angulos entre x e z)  e angulo desejado for maior que 0.05 (nao eh 0 por causa de erros de precisao)
        while (Mathf.Abs(Mathf.DeltaAngle(transform.eulerAngles.y, targetAngle)) > 0.05f)
        {
            //funcao de mover o angulo referente em volta do eixo y (aka angulo entre x e z) e angulo desejado [aumentando a velocidade o "salto" por frame eh maior)
            float angle = Mathf.MoveTowardsAngle(transform.eulerAngles.y, targetAngle, turnSpeed * Time.deltaTime);
            //coloca o novo valor de angulo na angulacao do objeto. up -> (0,1,0) pois nao queremos mudar as posicoes de x e z em relacao ao y, apenas os valores em relacao ao y. 
            transform.eulerAngles = Vector3.up * angle;

            yield return null;

        }
    }

    IEnumerator FollowPath(Vector3[] waypoints)
    {
        //objeto esta na posicao do primeiro waypoint
        transform.position = waypoints[0];

        int targetWaypointIndex = 1;
        //proximo caminho estara na posicao do proximo waypoint
        Vector3 targetWaypoint = waypoints[targetWaypointIndex];



        while (true)
        {
            // posicao atual move para a posicao do targetwaypoint na velocidade Speed
            transform.position = Vector3.MoveTowards(transform.position, targetWaypoint, Speed * Time.deltaTime);

            transform.LookAt(targetWaypoint);


            //Quando chegar na posicao desejada...
            if (transform.position == targetWaypoint)
            {
                //atualiza o index para a proxima posicao (quando chegar na ultima, zera)
                targetWaypointIndex = (targetWaypointIndex + 1) % waypoints.Length;
                //atualiza o target waypoint com a proxima posicao desejada
                targetWaypoint = waypoints[targetWaypointIndex];
                //espera por waitTime segundos.

                yield return new WaitForSeconds(waitTime);
                yield return StartCoroutine(TurnToFace(targetWaypoint));
            }
            //yield return garante que quando a funcao for chamada de novo, vai continuar a partir da proxima linha depois do return. Que loucura
            yield return null; //se retorno for null, vai voltar a rodar no proximo frame.

        }

    }


    private void Update()
    {
        //vai contanto tempo quando jogador for visto. Caso o tempo passar do limite, executa evento OnGuardHasSpottedPlayer()
        if (canSeePlayer())
        {
            //spotlight.color = Color.red;
            playerVisibleTimer += Time.deltaTime;
        }
        else
        {
            //playerVisibleTimer += Time.deltaTime;
            spotlight.color = originalColor;
        }
        playerVisibleTimer = Mathf.Clamp(playerVisibleTimer,0,timeToSpotPlayer);
        spotlight.color = Color.Lerp(originalColor, Color.red, playerVisibleTimer / timeToSpotPlayer);

        if(playerVisibleTimer >= timeToSpotPlayer)
        {
            if(OnGuardHasSpottedPlayer != null)
            {
                OnGuardHasSpottedPlayer();
            }
        }

    }


}







