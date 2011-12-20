using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;

namespace Zuliaworks.Netzuela.Paris.ContratoValeria
{
    [ServiceContract]
    public interface IValeria
    {
        [OperationContractAttribute(AsyncPattern = true)]
        IAsyncResult BeginEnviarTablas(DataSetXML Tabla, AsyncCallback Retorno, object EstadoAsincronico);
        bool EndEnviarTablas(IAsyncResult Resultado);

        [OperationContractAttribute(AsyncPattern = true)]
        IAsyncResult BeginRecibirTablas(AsyncCallback Retorno, object EstadoAsincronico);
        DataSetXML EndRecibirTablas(IAsyncResult Resultado);        
    }

    /*
    [ServiceContract]
    public interface IValeria
    {
        [OperationContract]
        DataSet RecibirTablas();
        [OperationContract]
        void EnviarTablas(string EsquemaXML, string XML);
    }
    */
}
