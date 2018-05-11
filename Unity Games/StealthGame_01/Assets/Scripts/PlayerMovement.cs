using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{

    public Rigidbody rb;
    public float Speed = 10f;
    public float smoothMoveTime = 0.1f; //tempo de atualizacao 
    public float turnSpeed = 8;
    public static event System.Action WinLevel;



    private float Smoothangle;
    private float smoothInputMagnitude;
    private float smoothMoveVelocity; //velocidade da suavizacao
    private Vector3 velocityrb;

    bool disabled = false;



    private void Start()
    {
        disabled = false;
        //quando um guarda espotar o jogador, a funcao "evento" (Onguard...) é sobrescrita pela funcao Disable, que vai fazer o jogador parar de andar
        Guard.OnGuardHasSpottedPlayer += Disable;


    }


    private void Disable()
    {
        disabled = true;
    }


    //quando o objeto é destruido, da unlink do evento para a funcao Disable. É bom fazer isso quando uma cena é recarregada no final do jogo
    void OnDestroy()
    {
        Guard.OnGuardHasSpottedPlayer -= Disable;
    }

    void Update ()
    {
        //Andando aplicando uma força.
        //rb.AddForce(Input.GetAxis("Horizontal") * Speed * Time.deltaTime, 0f, Input.GetAxis("Vertical")*Speed*Time.deltaTime);

        //vetor com o input
        //Vector3 inputDirection = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));

        Vector3 inputDirection = Vector3.zero;

        //caso o jogador nao for pego, ele vai poder continuar andando.
        if(!disabled)
        {
            inputDirection = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        }


        //magnitude do vetor de input. Usado na movimentacao
        float inputMagnitude = inputDirection.magnitude;


        //smoothdamp => varia o valor para um valor desejado com o tempo. No caso, varia o valor de smoth input magnitude para o inputmagnityude na velocidade, dando um tempo entre atualizacao smoothmovetime
        smoothInputMagnitude = Mathf.SmoothDamp(smoothInputMagnitude, inputMagnitude, ref smoothMoveVelocity, smoothMoveTime);



        //jogador encara a posicao que quer andar. Semelhante ao comportamento de rotacao do guarda.
        float targetAngle = Mathf.Atan2(inputDirection.x, inputDirection.z) * Mathf.Rad2Deg;


        //Quando solta, o angulo reseta pra 0 (global),entao usar lerp (interpola entre 2 valores, no caso angulos)
        //smooth turning: angle;
        //input magnitude multiplicando impede que o o angulo mude para 0 no final da movimentacao.
        Smoothangle = Mathf.LerpAngle(Smoothangle, targetAngle, Time.deltaTime * turnSpeed*inputMagnitude);
        ///transform.eulerAngles = Vector3.up * Smoothangle;

        //sem reset do angulo quando parado.
        //transform.eulerAngles = Vector3.up * targetAngle;




        /*
         * Movimentacao do bloco: Com a movimentacao do angulo acima, o bloco esta sempre olhando para frente, independente das posicao.
         * Desta forma, toda vez que a for andar pra frente, vai levar em consideracao a posicao do eulerAngles . Como o eulerAngles depende
         * do input, ao mexer o controle, varia o angulo. Consequentemente, a nocao de "pra frente" muda.
         * Usando a funcao translate, aplicamos o "andar pra frente" em relacao aos eixos do mundo. Desta forma, andar pra frente vai pegar os angulos
         * setados e traduzir para o mundo, sabendo assim, pra qual direcao andar :) 
         transform.forward => vetor(x,y,z) que vai indicar a movimentacao do objeto. Se for para a esquerda, por ex, vai ficar (-1,0,0)
         */

        //sem suavizacao durante a curva.
        //transform.Translate(transform.forward * Speed * Time.deltaTime * inputMagnitude, Space.World);

        //com suavizacao durante a curva.
        ///transform.Translate(transform.forward * Speed * Time.deltaTime * smoothInputMagnitude, Space.World);
        //transform.Translate(inputDirection * Speed * Time.deltaTime * inputMagnitude, Space.World); //isso moveria o bloco sem mexer a cabeça. para funcionar bem, comentar a linha da angulacao


        //Para movimentacao usando o rigidbody, comentar o controle transform.eulerAngles e tranform.Translate.
        //Controle de velocidade. Para frente(normalizado) * velocidade setada * a magnitude smooth do input .
        velocityrb = transform.forward * Speed * smoothInputMagnitude;
    }

    private void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Finish")
        {
            Disable();
            if (WinLevel != null)
                WinLevel();


        }
    }
    void FixedUpdate()
    {
        //seta a rotacao para o angulo calculado no update.
        rb.MoveRotation(Quaternion.Euler(Vector3.up * Smoothangle));
        rb.MovePosition(rb.position + velocityrb * Time.deltaTime);
    }
}
